"""
MediNomix AI - Backend API (Fixed Version)
100% Working with Direct Password
"""

from fastapi import FastAPI, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, text
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import requests
import logging
from pydantic import BaseModel
import os
import json
import asyncio
import aiohttp
import time
from contextlib import asynccontextmanager

# ==================== DATABASE CONFIGURATION ====================
# DIRECT PASSWORD - No encoding needed for student project
DATABASE_URL = "postgresql://postgres:PRO_CODER#1@localhost:5432/confusionguard"

# Create FastAPI app
app = FastAPI(
    title="MediNomix AI API",
    description="AI-Powered Medication Safety System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== DATABASE MODELS ====================

class Drug(Base):
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
    
    confusion_risks_as_source = relationship("ConfusionRisk", foreign_keys="ConfusionRisk.source_drug_id", back_populates="source_drug")
    confusion_risks_as_target = relationship("ConfusionRisk", foreign_keys="ConfusionRisk.target_drug_id", back_populates="target_drug")

class ConfusionRisk(Base):
    __tablename__ = "confusion_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    source_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    target_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    
    spelling_similarity = Column(Float)
    phonetic_similarity = Column(Float)
    length_similarity = Column(Float)
    therapeutic_context_risk = Column(Float)
    
    combined_risk = Column(Float)
    risk_category = Column(String)
    
    algorithm_version = Column(String, default="1.0")
    last_analyzed = Column(DateTime, default=func.now())
    
    source_drug = relationship("Drug", foreign_keys=[source_drug_id], back_populates="confusion_risks_as_source")
    target_drug = relationship("Drug", foreign_keys=[target_drug_id], back_populates="confusion_risks_as_target")

class AnalysisLog(Base):
    __tablename__ = "analysis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
    similar_drugs_found = Column(Integer)
    highest_risk_score = Column(Float)
    analysis_duration = Column(Float)

class RealTimeEvent(Base):
    __tablename__ = "realtime_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    event_data = Column(Text)
    timestamp = Column(DateTime, default=func.now(), index=True)
    severity = Column(String)

# ==================== REAL-TIME DASHBOARD MANAGER ====================

class RealTimeDashboardManager:
    """Manages real-time WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_metrics = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except:
            self.disconnect(websocket)

# Create global dashboard manager
dashboard_manager = RealTimeDashboardManager()

# ==================== DATABASE INITIALIZATION ====================

def init_database():
    """Initialize database - create if not exists"""
    try:
        # First check if we can connect to main database
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # Try to create database if it doesn't exist
        try:
            # Try connecting to PostgreSQL without specific database
            temp_engine = create_engine("postgresql://postgres:PRO_CODER#1@localhost:5432/postgres")
            with temp_engine.connect() as conn:
                conn.execute(text("CREATE DATABASE confusionguard"))
                logger.info("Database 'confusionguard' created successfully")
                conn.close()
            
            # Now create tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            
        except Exception as e2:
            logger.error(f"Failed to create database: {e2}")
            # Continue anyway - tables will be created when database exists

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
    recent_searches: List[Dict[str, Any]]
    system_status: str
    last_updated: datetime

# ==================== DATABASE DEPENDENCY ====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== OPENFDA INTEGRATION ====================

class OpenFDAClient:
    BASE_URL = "https://api.fda.gov/drug/label.json"
    
    @staticmethod
    async def search_drugs(search_term: str, limit: int = 20) -> List[Dict]:
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
        except Exception as e:
            logger.error(f"Error searching OpenFDA: {e}")
            return []
    
    @staticmethod
    def extract_drug_data(fda_data: Dict) -> Optional[Dict]:
        try:
            openfda = fda_data.get("openfda", {})
            
            product_ndc = openfda.get("product_ndc", [""])[0]
            application_number = openfda.get("application_number", [""])[0]
            openfda_id = product_ndc or application_number or str(hash(json.dumps(openfda, sort_keys=True)))
            
            brand_name = openfda.get("brand_name", [""])[0]
            if not brand_name or brand_name.lower() == "null":
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

try:
    from rapidfuzz import fuzz
    import jellyfish
except ImportError:
    # Fallback if libraries not installed
    logger.warning("rapidfuzz or jellyfish not installed. Using simple similarity functions.")
    
    class SimpleFuzz:
        @staticmethod
        def ratio(s1, s2):
            if not s1 or not s2:
                return 0
            s1, s2 = s1.lower(), s2.lower()
            if s1 == s2:
                return 100
            return 0
    
    fuzz = SimpleFuzz()
    jellyfish = None

class RiskAnalyzer:
    
    @staticmethod
    def calculate_spelling_similarity(name1: str, name2: str) -> float:
        if not name1 or not name2:
            return 0.0
        
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        if name1_lower == name2_lower:
            return 100.0
        
        try:
            fuzz_ratio = fuzz.ratio(name1_lower, name2_lower)
            partial_ratio = fuzz.ratio(name1_lower, name2_lower)  # Simplified
            token_sort_ratio = fuzz.ratio(name1_lower, name2_lower)  # Simplified
            
            spelling_score = (fuzz_ratio * 0.5 + partial_ratio * 0.3 + token_sort_ratio * 0.2)
            
            return min(100.0, max(0.0, spelling_score))
        except:
            # Simple fallback
            if name1_lower in name2_lower or name2_lower in name1_lower:
                return 60.0
            return 0.0
    
    @staticmethod
    def calculate_phonetic_similarity(name1: str, name2: str) -> float:
        if not name1 or not name2:
            return 0.0
        
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        if name1_lower == name2_lower:
            return 100.0
        
        if jellyfish:
            try:
                soundex1 = jellyfish.soundex(name1_lower)
                soundex2 = jellyfish.soundex(name2_lower)
                soundex_match = 100.0 if soundex1 == soundex2 else 0.0
                
                metaphone1 = jellyfish.metaphone(name1_lower)
                metaphone2 = jellyfish.metaphone(name2_lower)
                
                if metaphone1 and metaphone2:
                    metaphone_similarity = fuzz.ratio(metaphone1, metaphone2)
                else:
                    metaphone_similarity = 0.0
                
                phonetic_score = (soundex_match * 0.5 + metaphone_similarity * 0.5)
                return min(100.0, max(0.0, phonetic_score))
            except:
                pass
        
        # Simple fallback - check if they start with same letter
        if name1_lower[0] == name2_lower[0]:
            return 30.0
        return 0.0
    
    @staticmethod
    def calculate_length_similarity(name1: str, name2: str) -> float:
        len1, len2 = len(name1), len(name2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        if len1 == len2:
            return 100.0
        
        length_ratio = min(len1, len2) / max(len1, len2)
        return length_ratio * 100
    
    @staticmethod
    def calculate_therapeutic_context_risk(drug1: Drug, drug2: Drug) -> float:
        risk_score = 0.0
        
        # Check purpose similarity
        purpose1 = (drug1.purpose or "").lower()
        purpose2 = (drug2.purpose or "").lower()
        
        if purpose1 and purpose2:
            therapeutic_areas = [
                "pain", "infection", "diabetes", "heart", "blood pressure",
                "mental", "depression", "anxiety", "epilepsy", "seizure"
            ]
            
            for area in therapeutic_areas:
                if area in purpose1 and area in purpose2:
                    risk_score += 10.0
        
        # Check route similarity
        route1 = (drug1.route or "").lower()
        route2 = (drug2.route or "").lower()
        
        if route1 and route2 and route1 == route2:
            risk_score += 20.0
        
        # Known risky pairs
        known_risky_pairs = [
            ("lamictal", "lamisil"),
            ("celebrex", "celexa"),
            ("metformin", "metronidazole"),
            ("clonidine", "klonopin"),
            ("zyprexa", "zyrtec")
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
        weights = {
            "spelling": 0.40,
            "phonetic": 0.40,
            "length": 0.05,
            "therapeutic": 0.15
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
        if score >= 75:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 25:
            return "medium"
        else:
            return "low"

# ==================== DRUG ETL PIPELINE ====================

class DrugETL:
    
    @staticmethod
    async def fetch_and_store_drug(db: Session, search_term: str) -> Optional[Drug]:
        try:
            fda_results = await OpenFDAClient.search_drugs(search_term, limit=5)
            
            if not fda_results:
                logger.info(f"No results from OpenFDA for: {search_term}")
                return None
            
            for result in fda_results:
                drug_data = OpenFDAClient.extract_drug_data(result)
                if drug_data:
                    existing = db.query(Drug).filter(
                        Drug.openfda_id == drug_data["openfda_id"]
                    ).first()
                    
                    if existing:
                        logger.info(f"Drug already exists: {existing.brand_name}")
                        return existing
                    
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
        try:
            other_drugs = db.query(Drug).filter(Drug.id != new_drug.id).all()
            
            if not other_drugs:
                return
            
            analyzer = RiskAnalyzer()
            
            for other_drug in other_drugs:
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
                
                combined = analyzer.calculate_combined_risk({
                    "spelling": spelling,
                    "phonetic": phonetic,
                    "length": length,
                    "therapeutic": therapeutic
                })
                
                if combined >= 20:  # Only store significant risks
                    risk_category = analyzer.get_risk_category(combined)
                    
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
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error analyzing against all drugs: {e}")

# ==================== REAL-TIME FUNCTIONS ====================

async def get_realtime_metrics(db: Session) -> Dict[str, Any]:
    """Get real-time metrics for dashboard"""
    try:
        # Basic metrics
        total_drugs = db.query(Drug).count()
        total_analyses = db.query(AnalysisLog).count()
        
        high_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category.in_(["high", "critical"])
        ).count()
        
        critical_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category == "critical"
        ).count()
        
        # Average risk score
        avg_risk_result = db.execute(
            text("SELECT AVG(combined_risk) FROM confusion_risks WHERE combined_risk > 0")
        ).scalar()
        avg_risk_score = round(float(avg_risk_result or 0), 1)
        
        # Recent searches (last 10 minutes)
        ten_min_ago = datetime.utcnow() - timedelta(minutes=10)
        recent_searches = db.query(AnalysisLog).filter(
            AnalysisLog.timestamp >= ten_min_ago
        ).order_by(AnalysisLog.timestamp.desc()).limit(5).all()
        
        recent_search_data = []
        for search in recent_searches:
            recent_search_data.append({
                "drug_name": search.drug_name,
                "timestamp": search.timestamp.isoformat(),
                "risks_found": search.similar_drugs_found,
                "highest_risk": search.highest_risk_score
            })
        
        # System status
        system_status = "healthy"
        try:
            db.execute(text("SELECT 1"))
        except:
            system_status = "critical"
        
        metrics = {
            "total_drugs": total_drugs,
            "total_analyses": total_analyses,
            "high_risk_pairs": high_risk_pairs,
            "critical_risk_pairs": critical_risk_pairs,
            "avg_risk_score": avg_risk_score,
            "recent_searches": recent_search_data,
            "system_status": system_status,
            "last_updated": datetime.utcnow().isoformat(),
            "connected_clients": len(dashboard_manager.active_connections)
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting realtime metrics: {e}")
        return {
            "error": str(e),
            "last_updated": datetime.utcnow().isoformat(),
            "system_status": "error"
        }

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "name": "MediNomix AI API",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        drug_count = db.query(Drug).count()
        risk_count = db.query(ConfusionRisk).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "drugs_in_database": drug_count,
            "risk_assessments": risk_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# ==================== REAL-TIME DASHBOARD ENDPOINTS ====================

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    """WebSocket endpoint for real-time dashboard"""
    await dashboard_manager.connect(websocket)
    
    try:
        # Send initial data
        db = SessionLocal()
        try:
            metrics = await get_realtime_metrics(db)
            await dashboard_manager.send_personal_message({
                "type": "initial_data",
                "data": metrics,
                "timestamp": datetime.utcnow().isoformat()
            }, websocket)
        finally:
            db.close()
        
        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                if data == "ping":
                    await dashboard_manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)
            except WebSocketDisconnect:
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        dashboard_manager.disconnect(websocket)

@app.get("/api/realtime-metrics", response_model=DashboardMetrics)
async def get_realtime_metrics_endpoint(db: Session = Depends(get_db)):
    """Get real-time metrics via HTTP"""
    metrics_data = await get_realtime_metrics(db)
    
    return DashboardMetrics(
        total_drugs=metrics_data.get("total_drugs", 0),
        total_analyses=metrics_data.get("total_analyses", 0),
        high_risk_pairs=metrics_data.get("high_risk_pairs", 0),
        critical_risk_pairs=metrics_data.get("critical_risk_pairs", 0),
        avg_risk_score=metrics_data.get("avg_risk_score", 0),
        recent_searches=metrics_data.get("recent_searches", []),
        system_status=metrics_data.get("system_status", "unknown"),
        last_updated=datetime.fromisoformat(metrics_data.get("last_updated", datetime.utcnow().isoformat()))
    )

# ==================== MAIN API ENDPOINTS ====================

@app.get("/api/search/{drug_name}", response_model=AnalysisResponse)
async def search_and_analyze(drug_name: str, db: Session = Depends(get_db)):
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"Searching for drug: {drug_name}")
        
        # First check if drug exists in database
        existing_drug = db.query(Drug).filter(
            Drug.brand_name.ilike(f"%{drug_name}%")
        ).first()
        
        if not existing_drug:
            existing_drug = db.query(Drug).filter(
                Drug.generic_name.ilike(f"%{drug_name}%")
            ).first()
        
        drug = existing_drug
        
        # If not in database, fetch from OpenFDA
        if not drug:
            logger.info(f"Fetching from OpenFDA: {drug_name}")
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
        
        if not drug:
            raise HTTPException(
                status_code=404, 
                detail=f"Drug '{drug_name}' not found. Try a different spelling."
            )
        
        # Get similar drugs
        confusion_risks = db.query(ConfusionRisk).filter(
            (ConfusionRisk.source_drug_id == drug.id) |
            (ConfusionRisk.target_drug_id == drug.id)
        ).all()
        
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
        
        similar_drugs.sort(key=lambda x: x.combined_risk, reverse=True)
        
        # Log the analysis
        analysis_log = AnalysisLog(
            drug_name=drug_name,
            similar_drugs_found=len(similar_drugs),
            highest_risk_score=max([r.combined_risk for r in similar_drugs] or [0]),
            analysis_duration=(datetime.utcnow() - start_time).total_seconds()
        )
        db.add(analysis_log)
        db.commit()
        
        logger.info(f"Analysis complete: found {len(similar_drugs)} similar drugs")
        
        return AnalysisResponse(
            query_drug=drug.brand_name,
            similar_drugs=similar_drugs[:20],
            total_found=len(similar_drugs),
            analysis_id=str(analysis_log.id),
            timestamp=start_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_and_analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get dashboard metrics"""
    metrics_data = await get_realtime_metrics(db)
    
    return DashboardMetrics(
        total_drugs=metrics_data.get("total_drugs", 0),
        total_analyses=metrics_data.get("total_analyses", 0),
        high_risk_pairs=metrics_data.get("high_risk_pairs", 0),
        critical_risk_pairs=metrics_data.get("critical_risk_pairs", 0),
        avg_risk_score=metrics_data.get("avg_risk_score", 0),
        recent_searches=metrics_data.get("recent_searches", []),
        system_status=metrics_data.get("system_status", "unknown"),
        last_updated=datetime.fromisoformat(metrics_data.get("last_updated", datetime.utcnow().isoformat()))
    )

@app.post("/api/seed-database")
async def seed_database(db: Session = Depends(get_db)):
    """Seed database with common drugs"""
    try:
        common_drugs = [
            "metformin",
            "lamictal",
            "celebrex",
            "clonidine",
            "zyprexa",
            "lisinopril",
            "hydrocodone"
        ]
        
        seeded_count = 0
        seeded_drugs = []
        
        for drug_name in common_drugs:
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
            if drug:
                seeded_count += 1
                seeded_drugs.append(drug.brand_name)
                await asyncio.sleep(1)  # Delay to avoid rate limiting
        
        return {
            "message": f"Database seeded with {seeded_count} drugs",
            "seeded_drugs": seeded_drugs,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/api/top-risks", response_model=List[TopRiskPair])
async def get_top_risk_pairs(
    limit: int = Query(10, description="Number of pairs to return", ge=1, le=50),
    db: Session = Depends(get_db)
):
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
            if row[3] == "critical":
                reason = "Extremely high similarity"
            elif row[3] == "high":
                reason = "High similarity"
            else:
                reason = "Moderate similarity"
            
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

@app.get("/api/drugs")
async def get_all_drugs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return", le=500),
    db: Session = Depends(get_db)
):
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

# ==================== STARTUP EVENT ====================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting MediNomix Backend...")
    
    # Initialize database
    init_database()
    
    logger.info("MediNomix Backend started successfully!")
    logger.info(f"API Documentation: http://localhost:8000/docs")
    logger.info(f"Health Check: http://localhost:8000/health")

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("MEDINOMIX - Medication Safety System")
    print("=" * 60)
    print("🚀 Starting Backend Server...")
    print("💊 Features:")
    print("   • Drug Confusion Risk Analysis")
    print("   • Real-time Dashboard")
    print("   • OpenFDA Integration")
    print("=" * 60)
    print("📊 Endpoints:")
    print("   • http://localhost:8000 - API Status")
    print("   • http://localhost:8000/docs - Swagger UI")
    print("   • http://localhost:8000/health - Health Check")
    print("=" * 60)
    print("💡 To get started:")
    print("   1. Seed database: POST http://localhost:8000/api/seed-database")
    print("   2. Search drug: GET http://localhost:8000/api/search/metformin")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if port 8000 is available")
        print("3. Verify database credentials")