"""
ConfusionGuard AI - Backend API
FastAPI backend with OpenFDA integration and risk algorithms
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, text
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests
import logging
from pydantic import BaseModel
import os
import json
import asyncio
import aiohttp
import urllib.parse

# ----------------- Database Configuration -----------------
# URL encode the password to handle special characters
password = "PRO_CODER#1"
encoded_password = urllib.parse.quote(password)

# Database URL with encoded password
DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost:5432/confusionguard"

# Create FastAPI app
app = FastAPI(
    title="ConfusionGuard AI API",
    description="API for medication confusion risk analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATABASE MODELS ====================

class Drug(Base):
    """Drug information from OpenFDA"""
    __tablename__ = "drugs"
    
    id = Column(Integer, primary_key=True, index=True)
    openfda_id = Column(String, unique=True, index=True)
    brand_name = Column(String, index=True)
    generic_name = Column(String, index=True)
    manufacturer = Column(String)
    substance_name = Column(String)
    product_type = Column(String)
    route = Column(String)
    active_ingredients = Column(Text)
    purpose = Column(Text)
    warnings = Column(Text)
    indications_and_usage = Column(Text)
    dosage_form = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    confusion_risks_as_source = relationship(
        "ConfusionRisk", 
        foreign_keys="ConfusionRisk.source_drug_id",
        back_populates="source_drug"
    )
    confusion_risks_as_target = relationship(
        "ConfusionRisk", 
        foreign_keys="ConfusionRisk.target_drug_id",
        back_populates="target_drug"
    )

class ConfusionRisk(Base):
    """Risk assessment between two drugs"""
    __tablename__ = "confusion_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    source_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    target_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    
    # Similarity scores (0-100)
    spelling_similarity = Column(Float)
    phonetic_similarity = Column(Float)
    length_similarity = Column(Float)
    therapeutic_context_risk = Column(Float)
    
    # Combined risk score
    combined_risk = Column(Float)
    
    # Risk category
    risk_category = Column(String)  # low, medium, high, critical
    
    # Analysis metadata
    algorithm_version = Column(String, default="1.0")
    last_analyzed = Column(DateTime, default=func.now())
    
    # Relationships
    source_drug = relationship("Drug", foreign_keys=[source_drug_id], back_populates="confusion_risks_as_source")
    target_drug = relationship("Drug", foreign_keys=[target_drug_id], back_populates="confusion_risks_as_target")

class AnalysisLog(Base):
    """Log of user analyses"""
    __tablename__ = "analysis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
    similar_drugs_found = Column(Integer)
    highest_risk_score = Column(Float)
    analysis_duration = Column(Float)

# ==================== DATABASE INITIALIZATION ====================

def init_database():
    """Initialize database - create if not exists"""
    try:
        # First, try to connect without specifying database to create it if needed
        admin_url = f"postgresql://postgres:{encoded_password}@localhost:5432/postgres"
        admin_engine = create_engine(admin_url)
        
        with admin_engine.connect() as conn:
            # Check if confusionguard database exists
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'confusionguard'"))
            exists = result.fetchone()
            
            if not exists:
                logger.info("Creating database 'confusionguard'...")
                conn.execute(text("COMMIT"))
                conn.execute(text("CREATE DATABASE confusionguard"))
                logger.info("Database 'confusionguard' created successfully")
        
        admin_engine.dispose()
        
        # Now create tables in confusionguard database
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # Try to create tables anyway (database might already exist)
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e2:
            logger.error(f"Failed to create tables: {e2}")
            raise

# ==================== PYDANTIC MODELS ====================

class DrugBase(BaseModel):
    id: int
    brand_name: str
    generic_name: str
    manufacturer: Optional[str] = None
    purpose: Optional[str] = None
    
    class Config:
        from_attributes = True

class ConfusionRiskBase(BaseModel):
    id: int
    target_drug: DrugBase
    spelling_similarity: float
    phonetic_similarity: float
    therapeutic_context_risk: float
    combined_risk: float
    risk_category: str
    
    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    query_drug: str
    similar_drugs: List[ConfusionRiskBase]
    total_found: int
    analysis_id: str
    timestamp: datetime

class HeatmapData(BaseModel):
    drug_names: List[str]
    risk_matrix: List[List[float]]
    risk_categories: List[List[str]]

class TopRiskPair(BaseModel):
    drug1: str
    drug2: str
    risk_score: float
    risk_category: str
    reason: str

class RiskBreakdown(BaseModel):
    category: str
    count: int
    percentage: float

class DashboardMetrics(BaseModel):
    total_drugs: int
    total_analyses: int
    high_risk_pairs: int
    critical_risk_pairs: int
    avg_risk_score: float

# ==================== DATABASE DEPENDENCY ====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== OPENFDA INTEGRATION ====================

class OpenFDAClient:
    """Client for interacting with OpenFDA API"""
    
    BASE_URL = "https://api.fda.gov/drug/label.json"
    
    @staticmethod
    async def search_drugs(search_term: str, limit: int = 20) -> List[Dict]:
        """Search for drugs in OpenFDA database"""
        try:
            params = {
                "search": f'(openfda.brand_name:"{search_term}" OR openfda.generic_name:"{search_term}" OR openfda.substance_name:"{search_term}")',
                "limit": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(OpenFDAClient.BASE_URL, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        logger.error(f"OpenFDA API error: {response.status}")
                        return []
        except asyncio.TimeoutError:
            logger.error("OpenFDA API request timed out")
            return []
        except Exception as e:
            logger.error(f"Error searching OpenFDA: {e}")
            return []
    
    @staticmethod
    def extract_drug_data(fda_data: Dict) -> Optional[Dict]:
        """Extract relevant fields from OpenFDA response"""
        try:
            openfda = fda_data.get("openfda", {})
            
            # Generate unique ID
            product_ndc = openfda.get("product_ndc", [""])[0]
            application_number = openfda.get("application_number", [""])[0]
            openfda_id = product_ndc or application_number or str(hash(json.dumps(openfda, sort_keys=True)))
            
            # Get brand name - try multiple fields
            brand_name = openfda.get("brand_name", [""])[0]
            if not brand_name or brand_name.lower() == "null":
                # Try generic name as fallback
                brand_name = openfda.get("generic_name", [""])[0] or f"Drug-{openfda_id[:8]}"
            
            drug = {
                "openfda_id": openfda_id,
                "brand_name": brand_name,
                "generic_name": openfda.get("generic_name", [""])[0] or "",
                "manufacturer": openfda.get("manufacturer_name", [""])[0] or "",
                "substance_name": openfda.get("substance_name", [""])[0] or "",
                "product_type": openfda.get("product_type", [""])[0] or "",
                "route": openfda.get("route", [""])[0] or "",
                "active_ingredients": ", ".join(openfda.get("active_ingredient", [])),
                "purpose": fda_data.get("purpose", [""])[0] if isinstance(fda_data.get("purpose"), list) else "",
                "warnings": fda_data.get("warnings", [""])[0] if isinstance(fda_data.get("warnings"), list) else "",
                "indications_and_usage": fda_data.get("indications_and_usage", [""])[0] if isinstance(fda_data.get("indications_and_usage"), list) else "",
                "dosage_form": openfda.get("dosage_form", [""])[0] or "",
            }
            
            return drug
        except Exception as e:
            logger.error(f"Error extracting drug data: {e}")
            return None

# ==================== RISK ALGORITHMS ====================
# Using rapidfuzz for all similarity calculations
from rapidfuzz import fuzz
import jellyfish

class RiskAnalyzer:
    """Analyzes confusion risk between drug names"""
    
    @staticmethod
    def calculate_spelling_similarity(name1: str, name2: str) -> float:
        """Calculate spelling similarity using rapidfuzz"""
        if not name1 or not name2:
            return 0.0
        
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        if name1_lower == name2_lower:
            return 100.0
        
        # 1. RapidFuzz ratio (primary metric)
        fuzz_ratio = fuzz.ratio(name1_lower, name2_lower)
        
        # 2. Partial ratio for substring matches
        partial_ratio = fuzz.partial_ratio(name1_lower, name2_lower)
        
        # 3. Token sort ratio (order insensitive)
        token_sort_ratio = fuzz.token_sort_ratio(name1_lower, name2_lower)
        
        # Weighted average
        spelling_score = (fuzz_ratio * 0.5 + partial_ratio * 0.3 + token_sort_ratio * 0.2)
        
        return min(100.0, max(0.0, spelling_score))
    
    @staticmethod
    def calculate_phonetic_similarity(name1: str, name2: str) -> float:
        """Calculate phonetic similarity using soundex and metaphone"""
        if not name1 or not name2:
            return 0.0
        
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        if name1_lower == name2_lower:
            return 100.0
        
        # Soundex comparison
        try:
            soundex1 = jellyfish.soundex(name1_lower)
            soundex2 = jellyfish.soundex(name2_lower)
            soundex_match = 100.0 if soundex1 == soundex2 else 0.0
        except:
            soundex_match = 0.0
        
        # Metaphone comparison
        try:
            metaphone1 = jellyfish.metaphone(name1_lower)
            metaphone2 = jellyfish.metaphone(name2_lower)
            
            # Calculate metaphone similarity using rapidfuzz
            if metaphone1 and metaphone2:
                metaphone_similarity = fuzz.ratio(metaphone1, metaphone2)
            else:
                metaphone_similarity = 0.0
        except:
            metaphone_similarity = 0.0
        
        # NYSIIS comparison
        try:
            nysiis1 = jellyfish.nysiis(name1_lower)
            nysiis2 = jellyfish.nysiis(name2_lower)
            nysiis_similarity = fuzz.ratio(nysiis1, nysiis2) if nysiis1 and nysiis2 else 0.0
        except:
            nysiis_similarity = 0.0
        
        # Weighted average
        phonetic_score = (
            soundex_match * 0.3 + 
            metaphone_similarity * 0.4 + 
            nysiis_similarity * 0.3
        )
        
        return min(100.0, max(0.0, phonetic_score))
    
    @staticmethod
    def calculate_length_similarity(name1: str, name2: str) -> float:
        """Calculate similarity based on name length"""
        len1, len2 = len(name1), len(name2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        if len1 == len2:
            return 100.0
        
        length_ratio = min(len1, len2) / max(len1, len2)
        return length_ratio * 100
    
    @staticmethod
    def calculate_therapeutic_context_risk(drug1: Drug, drug2: Drug) -> float:
        """Calculate risk based on therapeutic context"""
        risk_score = 0.0
        
        # Check if purposes are similar
        purpose1 = (drug1.purpose or "").lower()
        purpose2 = (drug2.purpose or "").lower()
        
        if purpose1 and purpose2:
            # Simple keyword matching for therapeutic areas
            therapeutic_areas = [
                "pain", "infection", "diabetes", "heart", "blood pressure",
                "mental", "depression", "anxiety", "epilepsy", "seizure",
                "fungal", "bacterial", "viral", "inflammation", "arthritis"
            ]
            
            area_matches = 0
            for area in therapeutic_areas:
                if area in purpose1 and area in purpose2:
                    area_matches += 1
            
            if area_matches > 0:
                risk_score += min(30.0, area_matches * 10.0)
        
        # Check route of administration
        route1 = (drug1.route or "").lower()
        route2 = (drug2.route or "").lower()
        
        if route1 and route2 and route1 == route2:
            risk_score += 20.0
        
        # Check dosage form
        dosage1 = (drug1.dosage_form or "").lower()
        dosage2 = (drug2.dosage_form or "").lower()
        
        if dosage1 and dosage2 and dosage1 == dosage2:
            risk_score += 20.0
        
        # Known high-risk pairs (based on FDA alerts)
        known_risky_pairs = [
            ("lamictal", "lamisil"),
            ("celebrex", "celexa"),
            ("metformin", "metronidazole"),
            ("clonidine", "klonopin"),
            ("zyprexa", "zyrtec"),
            ("seroquel", "serzone"),
            ("hydrocodone", "oxycodone"),
            ("morphine", "hydromorphone")
        ]
        
        brand1 = drug1.brand_name.lower()
        brand2 = drug2.brand_name.lower()
        
        for pair in known_risky_pairs:
            if (brand1 == pair[0] and brand2 == pair[1]) or (brand1 == pair[1] and brand2 == pair[0]):
                risk_score += 30.0
                break
        
        return min(100.0, risk_score)
    
    @staticmethod
    def calculate_combined_risk(scores: Dict) -> float:
        """Calculate combined risk score with weights"""
        weights = {
            "spelling": 0.40,    # Increased weight for spelling
            "phonetic": 0.40,    # Increased weight for phonetic
            "length": 0.05,      # Reduced weight for length
            "therapeutic": 0.15   # Reduced weight for therapeutic
        }
        
        combined = (
            scores.get("spelling", 0) * weights["spelling"] +
            scores.get("phonetic", 0) * weights["phonetic"] +
            scores.get("length", 0) * weights["length"] +
            scores.get("therapeutic", 0) * weights["therapeutic"]
        )
        
        return min(100.0, max(0.0, combined))
    
    @staticmethod
    def get_risk_category(score: float) -> str:
        """Convert risk score to category"""
        if score >= 75:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 25:
            return "medium"
        else:
            return "low"

# ==================== ETL PIPELINE ====================

class DrugETL:
    """ETL pipeline for drug data"""
    
    @staticmethod
    async def fetch_and_store_drug(db: Session, search_term: str) -> Optional[Drug]:
        """Fetch drug from OpenFDA and store in database"""
        try:
            # Search OpenFDA
            fda_results = await OpenFDAClient.search_drugs(search_term, limit=5)
            
            if not fda_results:
                logger.info(f"No results from OpenFDA for: {search_term}")
                return None
            
            # Process first relevant result
            for result in fda_results:
                drug_data = OpenFDAClient.extract_drug_data(result)
                if drug_data:
                    # Check if drug already exists
                    existing = db.query(Drug).filter(
                        Drug.openfda_id == drug_data["openfda_id"]
                    ).first()
                    
                    if existing:
                        logger.info(f"Drug already exists: {existing.brand_name}")
                        return existing
                    
                    # Create new drug record
                    drug = Drug(**drug_data)
                    db.add(drug)
                    db.commit()
                    db.refresh(drug)
                    
                    logger.info(f"Stored new drug: {drug.brand_name}")
                    
                    # Analyze against existing drugs
                    await DrugETL.analyze_against_all_drugs(db, drug)
                    
                    return drug
            
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error in fetch_and_store_drug: {e}")
            return None
    
    @staticmethod
    async def analyze_against_all_drugs(db: Session, new_drug: Drug):
        """Analyze new drug against all existing drugs"""
        try:
            # Get all other drugs
            other_drugs = db.query(Drug).filter(Drug.id != new_drug.id).all()
            
            if not other_drugs:
                return
            
            analyzer = RiskAnalyzer()
            risks_added = 0
            
            for other_drug in other_drugs:
                # Calculate all similarity scores
                spelling = analyzer.calculate_spelling_similarity(
                    new_drug.brand_name, other_drug.brand_name
                )
                phonetic = analyzer.calculate_phonetic_similarity(
                    new_drug.brand_name, other_drug.brand_name
                )
                length = analyzer.calculate_length_similarity(
                    new_drug.brand_name, other_drug.brand_name
                )
                therapeutic = analyzer.calculate_therapeutic_context_risk(
                    new_drug, other_drug
                )
                
                # Calculate combined risk
                combined = analyzer.calculate_combined_risk({
                    "spelling": spelling,
                    "phonetic": phonetic,
                    "length": length,
                    "therapeutic": therapeutic
                })
                
                # Only store if risk is significant
                if combined >= 20:
                    risk_category = analyzer.get_risk_category(combined)
                    
                    # Check if risk analysis already exists
                    existing = db.query(ConfusionRisk).filter(
                        ((ConfusionRisk.source_drug_id == new_drug.id) & 
                         (ConfusionRisk.target_drug_id == other_drug.id)) |
                        ((ConfusionRisk.source_drug_id == other_drug.id) & 
                         (ConfusionRisk.target_drug_id == new_drug.id))
                    ).first()
                    
                    if not existing:
                        confusion_risk = ConfusionRisk(
                            source_drug_id=new_drug.id,
                            target_drug_id=other_drug.id,
                            spelling_similarity=spelling,
                            phonetic_similarity=phonetic,
                            length_similarity=length,
                            therapeutic_context_risk=therapeutic,
                            combined_risk=combined,
                            risk_category=risk_category
                        )
                        
                        db.add(confusion_risk)
                        risks_added += 1
            
            if risks_added > 0:
                db.commit()
                logger.info(f"Added {risks_added} new risk assessments for {new_drug.brand_name}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error analyzing against all drugs: {e}")

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "ConfusionGuard AI API",
        "version": "1.0.0",
        "description": "Medication confusion risk analysis system",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "/health": "Health check",
            "/docs": "API documentation",
            "/api/search/{drug_name}": "Search and analyze drug",
            "/api/seed-database": "Seed with common drugs"
        }
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        # Get counts
        drug_count = db.query(Drug).count()
        risk_count = db.query(ConfusionRisk).count()
        analysis_count = db.query(AnalysisLog).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "drugs_in_database": drug_count,
            "risk_assessments": risk_count,
            "total_analyses": analysis_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/api/search/{drug_name}", response_model=AnalysisResponse)
async def search_and_analyze(
    drug_name: str,
    db: Session = Depends(get_db)
):
    """Search for a drug and analyze confusion risks"""
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"Searching for drug: {drug_name}")
        
        # Check if drug already exists in database (case-insensitive search)
        existing_drug = db.query(Drug).filter(
            Drug.brand_name.ilike(f"%{drug_name}%")
        ).first()
        
        # If not found by brand name, try generic name
        if not existing_drug:
            existing_drug = db.query(Drug).filter(
                Drug.generic_name.ilike(f"%{drug_name}%")
            ).first()
        
        drug = existing_drug
        
        # If not found in database, fetch from OpenFDA
        if not drug:
            logger.info(f"Drug not in database, fetching from OpenFDA: {drug_name}")
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
        
        # If still not found, try fuzzy search in existing drugs
        if not drug:
            logger.info(f"Trying fuzzy search for: {drug_name}")
            all_drugs = db.query(Drug).all()
            analyzer = RiskAnalyzer()
            best_match = None
            best_score = 0
            
            for d in all_drugs:
                score = analyzer.calculate_spelling_similarity(drug_name, d.brand_name)
                if score > best_score and score > 40:  # Lower threshold for fuzzy match
                    best_score = score
                    best_match = d
            
            drug = best_match
        
        if not drug:
            raise HTTPException(
                status_code=404, 
                detail=f"Drug '{drug_name}' not found in FDA database or local cache. Try a different spelling."
            )
        
        # Get confusion risks for this drug
        confusion_risks = db.query(ConfusionRisk).filter(
            (ConfusionRisk.source_drug_id == drug.id) |
            (ConfusionRisk.target_drug_id == drug.id)
        ).all()
        
        # Prepare response
        similar_drugs = []
        for risk in confusion_risks:
            if risk.source_drug_id == drug.id:
                target = risk.target_drug
            else:
                target = risk.source_drug
            
            similar_drugs.append(ConfusionRiskBase(
                id=risk.id,
                target_drug=DrugBase(
                    id=target.id,
                    brand_name=target.brand_name,
                    generic_name=target.generic_name,
                    manufacturer=target.manufacturer,
                    purpose=target.purpose[:100] + "..." if target.purpose and len(target.purpose) > 100 else target.purpose
                ),
                spelling_similarity=round(risk.spelling_similarity, 1),
                phonetic_similarity=round(risk.phonetic_similarity, 1),
                therapeutic_context_risk=round(risk.therapeutic_context_risk, 1),
                combined_risk=round(risk.combined_risk, 1),
                risk_category=risk.risk_category
            ))
        
        # Sort by combined risk (highest first)
        similar_drugs.sort(key=lambda x: x.combined_risk, reverse=True)
        
        # Log analysis
        analysis_log = AnalysisLog(
            drug_name=drug_name,
            similar_drugs_found=len(similar_drugs),
            highest_risk_score=max([r.combined_risk for r in similar_drugs] or [0]),
            analysis_duration=(datetime.utcnow() - start_time).total_seconds()
        )
        db.add(analysis_log)
        db.commit()
        
        logger.info(f"Analysis complete for {drug_name}: found {len(similar_drugs)} similar drugs")
        
        return AnalysisResponse(
            query_drug=drug.brand_name,
            similar_drugs=similar_drugs[:20],  # Limit to top 20
            total_found=len(similar_drugs),
            analysis_id=str(analysis_log.id),
            timestamp=start_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in search_and_analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/heatmap", response_model=HeatmapData)
async def get_heatmap_data(
    limit: int = Query(10, description="Number of drugs to include", ge=5, le=20),
    db: Session = Depends(get_db)
):
    """Get data for confusion heatmap"""
    try:
        # Get drugs with the most confusion risks
        query = text("""
            SELECT d.id, d.brand_name, COUNT(cr.id) as risk_count
            FROM drugs d
            LEFT JOIN confusion_risks cr ON d.id = cr.source_drug_id OR d.id = cr.target_drug_id
            GROUP BY d.id, d.brand_name
            HAVING COUNT(cr.id) > 0
            ORDER BY risk_count DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit})
        top_drugs = result.fetchall()
        
        if not top_drugs:
            # If no drugs with risks, get some drugs
            top_drugs = db.query(Drug.id, Drug.brand_name).limit(limit).all()
            
            if not top_drugs:
                return HeatmapData(
                    drug_names=[],
                    risk_matrix=[],
                    risk_categories=[]
                )
        
        drug_ids = [row[0] for row in top_drugs]
        drug_names = [row[1] for row in top_drugs]
        
        # Create risk matrix
        risk_matrix = []
        risk_categories = []
        
        for i, drug_id1 in enumerate(drug_ids):
            row = []
            category_row = []
            for j, drug_id2 in enumerate(drug_ids):
                if i == j:
                    row.append(0.0)
                    category_row.append("none")
                else:
                    # Find risk between these two drugs
                    risk = db.query(ConfusionRisk).filter(
                        ((ConfusionRisk.source_drug_id == drug_id1) & 
                         (ConfusionRisk.target_drug_id == drug_id2)) |
                        ((ConfusionRisk.source_drug_id == drug_id2) & 
                         (ConfusionRisk.target_drug_id == drug_id1))
                    ).first()
                    
                    if risk:
                        row.append(float(risk.combined_risk))
                        category_row.append(risk.risk_category)
                    else:
                        row.append(0.0)
                        category_row.append("none")
            
            risk_matrix.append(row)
            risk_categories.append(category_row)
        
        return HeatmapData(
            drug_names=drug_names,
            risk_matrix=risk_matrix,
            risk_categories=risk_categories
        )
        
    except Exception as e:
        logger.error(f"Error getting heatmap data: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/api/top-risks", response_model=List[TopRiskPair])
async def get_top_risk_pairs(
    limit: int = Query(10, description="Number of pairs to return", ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get top risk pairs"""
    try:
        query = text("""
            SELECT 
                d1.brand_name as drug1,
                d2.brand_name as drug2,
                cr.combined_risk,
                cr.risk_category
            FROM confusion_risks cr
            JOIN drugs d1 ON cr.source_drug_id = d1.id
            JOIN drugs d2 ON cr.target_drug_id = d2.id
            WHERE cr.combined_risk >= 30
            ORDER BY cr.combined_risk DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit})
        rows = result.fetchall()
        
        top_pairs = []
        for row in rows:
            # Create descriptive reason based on risk level
            if row[3] == "critical":
                reason = "Extremely high similarity - immediate attention required"
            elif row[3] == "high":
                reason = "High similarity - review required"
            else:
                reason = "Moderate similarity - monitor closely"
            
            top_pairs.append(TopRiskPair(
                drug1=row[0],
                drug2=row[1],
                risk_score=float(row[2]),
                risk_category=row[3],
                reason=reason
            ))
        
        return top_pairs
        
    except Exception as e:
        logger.error(f"Error getting top risks: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/api/risk-breakdown", response_model=List[RiskBreakdown])
async def get_risk_breakdown(db: Session = Depends(get_db)):
    """Get breakdown of risk categories"""
    try:
        query = text("""
            SELECT 
                risk_category,
                COUNT(*) as count
            FROM confusion_risks
            GROUP BY risk_category
            ORDER BY 
                CASE risk_category
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                    ELSE 5
                END
        """)
        
        result = db.execute(query)
        rows = result.fetchall()
        
        if not rows:
            # Return empty breakdown if no risks
            return []
        
        total = sum(row[1] for row in rows)
        
        breakdown = []
        for row in rows:
            category = row[0] if row[0] else "uncategorized"
            count = row[1]
            percentage = round((count / total * 100), 1) if total > 0 else 0
            
            breakdown.append(RiskBreakdown(
                category=category,
                count=count,
                percentage=percentage
            ))
        
        return breakdown
        
    except Exception as e:
        logger.error(f"Error getting risk breakdown: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/api/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get dashboard metrics"""
    try:
        total_drugs = db.query(Drug).count()
        total_analyses = db.query(AnalysisLog).count()
        
        high_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category.in_(["high", "critical"])
        ).count()
        
        critical_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category == "critical"
        ).count()
        
        # Calculate average risk score
        avg_risk_result = db.execute(
            text("SELECT AVG(combined_risk) FROM confusion_risks WHERE combined_risk > 0")
        ).scalar()
        avg_risk_score = round(float(avg_risk_result or 0), 1)
        
        return DashboardMetrics(
            total_drugs=total_drugs,
            total_analyses=total_analyses,
            high_risk_pairs=high_risk_pairs,
            critical_risk_pairs=critical_risk_pairs,
            avg_risk_score=avg_risk_score
        )
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.post("/api/seed-database")
async def seed_database(db: Session = Depends(get_db)):
    """Seed database with common high-risk drugs"""
    try:
        # Common high-risk drug pairs
        common_drugs = [
            "metformin",
            "metronidazole",
            "lamictal",
            "lamisil",
            "celebrex",
            "celexa",
            "clonidine",
            "klonopin",
            "zyprexa",
            "zyrtec",
            "seroquel",
            "serzone",
            "lisinopril",
            "hydrocodone",
            "oxycodone"
        ]
        
        seeded_count = 0
        for drug_name in common_drugs:
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
            if drug:
                seeded_count += 1
                await asyncio.sleep(0.5)  # Rate limiting for OpenFDA API
        
        return {
            "message": f"Database seeded with {seeded_count} drugs",
            "seeded_drugs": seeded_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/api/drugs")
async def get_all_drugs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return", le=500),
    db: Session = Depends(get_db)
):
    """Get all drugs in database"""
    try:
        drugs = db.query(Drug).offset(skip).limit(limit).all()
        
        return {
            "drugs": [
                {
                    "id": drug.id,
                    "brand_name": drug.brand_name,
                    "generic_name": drug.generic_name,
                    "manufacturer": drug.manufacturer,
                    "purpose": drug.purpose
                }
                for drug in drugs
            ],
            "total": db.query(Drug).count(),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting drugs: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("ConfusionGuard AI - Backend Server")
    print("=" * 60)
    
    try:
        # Initialize database (create if not exists)
        init_database()
        print("✅ Database initialized successfully")
        
        print(f"📊 Database: confusionguard")
        print(f"🔗 API Documentation: http://localhost:8000/docs")
        print(f"❤️  Health Check: http://localhost:8000/health")
        print("=" * 60)
        print("🚀 To get started:")
        print("1. Seed database: POST http://localhost:8000/api/seed-database")
        print("2. Search drug: GET http://localhost:8000/api/search/metformin")
        print("=" * 60)
        
        # Run the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("Troubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your password is correct")
        print("3. Verify PostgreSQL service is started")
        print("   Windows: Run 'services.msc' and start PostgreSQL")
        print("   Linux/Mac: 'sudo systemctl start postgresql'")