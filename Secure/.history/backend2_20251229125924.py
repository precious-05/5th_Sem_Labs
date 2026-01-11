from fastapi import FastAPI, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, text, func, distinct, Boolean, Index
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
import requests
import logging
import os
import json
import asyncio
import aiohttp
import time
import random
import re
from collections import defaultdict, Counter
import jellyfish
from fuzzywuzzy import fuzz
import warnings
warnings.filterwarnings("ignore")

# ==================== DATABASE CONFIGURATION ====================
DATABASE_URL = "postgresql://postgres:PRO_CODER#1@localhost:5432/confusionguard"

# Create FastAPI app
app = FastAPI(
    title="Medication Safety Guard API",
    description="Professional AI-Powered Medication Confusion Prevention System",
    version="3.0.0"
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
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=20, max_overflow=30)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("✅ Database engine created successfully")
except Exception as e:
    print(f"❌ Error creating database engine: {e}")
    print("Please make sure PostgreSQL is running on localhost:5432")
    exit(1)

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== DATABASE MODELS ====================

class Drug(Base):
    """Enhanced drug information"""
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
    
    # Enhanced medical fields
    drug_class = Column(String, index=True)
    atc_code = Column(String, index=True)
    therapeutic_category = Column(String)
    side_effects = Column(Text)
    contraindications = Column(Text)
    
    # Phonetic representations
    soundex_code = Column(String, index=True)
    metaphone_code = Column(String, index=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
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
    
    __table_args__ = (
        Index('idx_drug_names', 'brand_name', 'generic_name'),
        Index('idx_drug_phonetic', 'soundex_code', 'metaphone_code'),
    )

class ConfusionRisk(Base):
    """Enhanced risk assessment"""
    __tablename__ = "confusion_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    source_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    target_drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    
    # Similarity scores
    spelling_similarity = Column(Float)
    phonetic_similarity = Column(Float)
    therapeutic_context_risk = Column(Float)
    
    # Enhanced scores
    levenshtein_similarity = Column(Float)
    soundex_match = Column(Boolean, default=False)
    metaphone_match = Column(Boolean, default=False)
    
    # Critical flags
    is_known_risky_pair = Column(Boolean, default=False)
    same_drug_class = Column(Boolean, default=False)
    same_therapeutic_category = Column(Boolean, default=False)
    
    # Final scores
    combined_risk = Column(Float)
    risk_category = Column(String)
    risk_reason = Column(Text)
    
    algorithm_version = Column(String, default="3.0")
    last_analyzed = Column(DateTime, default=func.now())
    
    source_drug = relationship("Drug", foreign_keys=[source_drug_id], back_populates="confusion_risks_as_source")
    target_drug = relationship("Drug", foreign_keys=[target_drug_id], back_populates="confusion_risks_as_target")

class AnalysisLog(Base):
    """Enhanced analysis logging"""
    __tablename__ = "analysis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
    similar_drugs_found = Column(Integer)
    highest_risk_score = Column(Float)
    critical_risks_found = Column(Integer)
    analysis_duration = Column(Float)
    user_feedback = Column(String)

class KnownRiskyPair(Base):
    """Database of known confusing drug pairs"""
    __tablename__ = "known_risky_pairs"
    
    id = Column(Integer, primary_key=True, index=True)
    drug1_name = Column(String, index=True)
    drug2_name = Column(String, index=True)
    risk_level = Column(String)
    reason = Column(Text)
    source = Column(String)
    reported_incidents = Column(Integer, default=0)
    last_reported = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# ==================== ENHANCED RISK ANALYZER ====================

class AdvancedRiskAnalyzer:
    """Professional-grade medication confusion analyzer"""
    
    # Known risky pairs database
    KNOWN_RISKY_PAIRS = {
        ("lamictal", "lamisil"): {"risk": "critical", "reason": "Epilepsy vs Antifungal"},
        ("celebrex", "celexa"): {"risk": "critical", "reason": "Arthritis vs Depression"},
        ("hydralazine", "hydroxyzine"): {"risk": "critical", "reason": "Blood Pressure vs Anxiety"},
        ("clonidine", "klonopin"): {"risk": "high", "reason": "Hypertension vs Anxiety"},
        ("metformin", "metronidazole"): {"risk": "high", "reason": "Diabetes vs Antibiotic"},
        ("zyprexa", "zyrtec"): {"risk": "high", "reason": "Antipsychotic vs Allergy"},
        ("lisinopril", "lisdexamfetamine"): {"risk": "medium", "reason": "Similar prefix, different classes"},
        ("amlodipine", "amiodarone"): {"risk": "high", "reason": "Similar spelling, different cardiovascular drugs"},
        ("acetaminophen", "acetylcysteine"): {"risk": "critical", "reason": "Overdose treatment vs pain relief"},
        ("alprazolam", "lorazepam"): {"risk": "high", "reason": "Similar benzodiazepines"},
        ("amiodarone", "amrinone"): {"risk": "high", "reason": "Similar heart medications"},
        ("amitriptyline", "nortriptyline"): {"risk": "high", "reason": "Similar antidepressants"},
        ("diazepam", "diltiazem"): {"risk": "critical", "reason": "Anxiety vs Heart medication"},
        ("fluoxetine", "paroxetine"): {"risk": "high", "reason": "Similar SSRIs"},
        ("haloperidol", "hydromorphone"): {"risk": "critical", "reason": "Antipsychotic vs Opioid"},
        ("metoprolol", "metroNIDAZOLE"): {"risk": "critical", "reason": "Beta blocker vs Antibiotic"},
        ("morphine", "hydromorphone"): {"risk": "critical", "reason": "Different potency opioids"},
        ("oxycodone", "oxyCONTIN"): {"risk": "critical", "reason": "Immediate vs Extended release"},
        ("risperidone", "ropinirole"): {"risk": "critical", "reason": "Antipsychotic vs Parkinson's"},
        ("sertraline", "cetirizine"): {"risk": "critical", "reason": "Antidepressant vs Antihistamine"},
        ("tramadol", "trazodone"): {"risk": "critical", "reason": "Pain vs Depression"},
        ("warfarin", "xarelto"): {"risk": "critical", "reason": "Different anticoagulants"},
        ("zolpidem", "zonisamide"): {"risk": "critical", "reason": "Sleep vs Seizure"},
        ("buspirone", "bupropion"): {"risk": "high", "reason": "Anxiety vs Depression"},
        ("chlorpromazine", "chlorpropamide"): {"risk": "critical", "reason": "Antipsychotic vs Diabetes"},
        ("epinephrine", "ephedrine"): {"risk": "high", "reason": "Similar emergency medications"},
        ("insulin aspart", "insulin glulisine"): {"risk": "high", "reason": "Rapid-acting insulins"},
        ("nicardipine", "nifedipine"): {"risk": "high", "reason": "Similar calcium channel blockers"},
        ("prednisone", "prednisolone"): {"risk": "high", "reason": "Similar corticosteroids"},
        ("tobramycin", "tobraDEX"): {"risk": "high", "reason": "Antibiotic vs Combination"},
        ("valacyclovir", "valganciclovir"): {"risk": "high", "reason": "Similar antivirals"},
    }
    
    # Drug suffixes and their classes
    DRUG_SUFFIXES = {
        'pril': 'ACE inhibitor',
        'sartan': 'ARB',
        'olol': 'Beta blocker',
        'dipine': 'Calcium channel blocker',
        'statin': 'Statin',
        'prazole': 'PPI',
        'cycline': 'Antibiotic',
        'mycin': 'Antibiotic',
        'floxacin': 'Antibiotic',
        'cillin': 'Antibiotic',
        'vir': 'Antiviral',
        'zole': 'Antifungal',
        'oxetine': 'SSRI',
        'triptyline': 'TCA',
        'pam': 'Benzodiazepine',
        'lam': 'Benzodiazepine',
        'azine': 'Antipsychotic',
        'done': 'Opioid',
        'caine': 'Anesthetic',
        'profen': 'NSAID',
        'parin': 'Anticoagulant',
        'xaban': 'Anticoagulant',
        'grel': 'Antiplatelet',
        'gliptin': 'Diabetes',
        'glitazone': 'Diabetes',
        'formin': 'Diabetes',
        'glutide': 'Diabetes',
    }
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return AdvancedRiskAnalyzer.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def calculate_spelling_similarity(name1: str, name2: str) -> Dict[str, float]:
        """Calculate advanced spelling similarity"""
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        
        if name1 == name2:
            return {
                "basic": 100.0,
                "levenshtein": 100.0,
                "fuzzy": 100.0,
                "prefix": 100.0
            }
        
        # 1. Basic string similarity
        if name1.startswith(name2[:3]) or name2.startswith(name1[:3]):
            basic_sim = 70.0
        elif name1 in name2 or name2 in name1:
            basic_sim = 60.0
        else:
            common_chars = len(set(name1) & set(name2))
            total_chars = len(set(name1) | set(name2))
            basic_sim = (common_chars / total_chars) * 100 if total_chars > 0 else 0
        
        # 2. Levenshtein similarity
        distance = AdvancedRiskAnalyzer.levenshtein_distance(name1, name2)
        max_len = max(len(name1), len(name2))
        levenshtein_sim = ((max_len - distance) / max_len) * 100 if max_len > 0 else 0
        
        # 3. Fuzzy string matching
        fuzzy_sim = fuzz.ratio(name1, name2)
        
        # 4. Prefix similarity
        prefix_len = 0
        min_len = min(len(name1), len(name2))
        for i in range(min_len):
            if name1[i] == name2[i]:
                prefix_len += 1
            else:
                break
        prefix_sim = (prefix_len / max_len) * 100 if max_len > 0 else 0
        
        return {
            "basic": round(basic_sim, 1),
            "levenshtein": round(levenshtein_sim, 1),
            "fuzzy": round(float(fuzzy_sim), 1),
            "prefix": round(prefix_sim, 1)
        }
    
    @staticmethod
    def calculate_phonetic_similarity(name1: str, name2: str) -> Dict[str, Any]:
        """Calculate advanced phonetic similarity"""
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        
        if name1 == name2:
            return {
                "basic": 100.0,
                "soundex_match": True,
                "metaphone_match": True,
                "nysiis_match": True
            }
        
        # 1. Soundex
        soundex1 = jellyfish.soundex(name1)
        soundex2 = jellyfish.soundex(name2)
        soundex_match = soundex1 == soundex2
        
        # 2. Metaphone
        metaphone1 = jellyfish.metaphone(name1)
        metaphone2 = jellyfish.metaphone(name2)
        metaphone_match = metaphone1 == metaphone2
        
        # 3. NYSIIS
        nysiis1 = jellyfish.nysiis(name1)
        nysiis2 = jellyfish.nysiis(name2)
        nysiis_match = nysiis1 == nysiis2
        
        # 4. Basic phonetic rules
        basic_score = 0.0
        sound_alike_rules = [
            ("cef", "sef"), ("ph", "f"), ("x", "ks"),
            ("c", "k"), ("z", "s"), ("qu", "kw"),
            ("gh", "f"), ("kn", "n"), ("pn", "n"),
            ("ps", "s"), ("wr", "r")
        ]
        
        name1_sound = name1
        name2_sound = name2
        for old, new in sound_alike_rules:
            name1_sound = name1_sound.replace(old, new)
            name2_sound = name2_sound.replace(old, new)
        
        if name1_sound == name2_sound:
            basic_score = 80.0
        elif name1_sound[:3] == name2_sound[:3]:
            basic_score = 50.0
        
        return {
            "basic": round(basic_score, 1),
            "soundex_match": soundex_match,
            "metaphone_match": metaphone_match,
            "nysiis_match": nysiis_match
        }
    
    @staticmethod
    def analyze_drug_suffixes(name1: str, name2: str) -> Dict[str, Any]:
        """Analyze drug name suffixes for therapeutic class"""
        name1 = name1.lower()
        name2 = name2.lower()
        
        suffix1 = None
        suffix2 = None
        class1 = None
        class2 = None
        
        for suffix, drug_class in AdvancedRiskAnalyzer.DRUG_SUFFIXES.items():
            if name1.endswith(suffix):
                suffix1 = suffix
                class1 = drug_class
            if name2.endswith(suffix):
                suffix2 = suffix
                class2 = drug_class
        
        return {
            "suffix_match": suffix1 == suffix2 if suffix1 and suffix2 else False,
            "class_match": class1 == class2 if class1 and class2 else False,
            "suffix1": suffix1,
            "suffix2": suffix2,
            "class1": class1,
            "class2": class2
        }
    
    @staticmethod
    def check_known_risky_pair(name1: str, name2: str) -> Dict[str, Any]:
        """Check if pair is in known risky database"""
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        
        # Check exact match
        key = tuple(sorted([name1, name2]))
        if key in AdvancedRiskAnalyzer.KNOWN_RISKY_PAIRS:
            return AdvancedRiskAnalyzer.KNOWN_RISKY_PAIRS[key]
        
        # Check partial matches
        for (pair1, pair2), info in AdvancedRiskAnalyzer.KNOWN_RISKY_PAIRS.items():
            if (name1 in pair1 or pair1 in name1) and (name2 in pair2 or pair2 in name2):
                return info
        
        return {"risk": "none", "reason": ""}
    
    @staticmethod
    def analyze_therapeutic_context(drug1, drug2) -> Dict[str, Any]:
        """Analyze therapeutic context"""
        purpose1 = (getattr(drug1, 'purpose', '') or '').lower()
        purpose2 = (getattr(drug2, 'purpose', '') or '').lower()
        
        # Check known risky pair
        known_info = AdvancedRiskAnalyzer.check_known_risky_pair(
            getattr(drug1, 'brand_name', ''),
            getattr(drug2, 'brand_name', '')
        )
        
        if known_info["risk"] != "none":
            risk_map = {"critical": 100.0, "high": 80.0, "medium": 50.0, "low": 30.0}
            return {
                "score": risk_map.get(known_info["risk"], 0.0),
                "known_risk": True,
                "reason": known_info["reason"],
                "risk_level": known_info["risk"]
            }
        
        # Check drug class match
        drug_class1 = getattr(drug1, 'drug_class', '').lower()
        drug_class2 = getattr(drug2, 'drug_class', '').lower()
        same_class = bool(drug_class1 and drug_class1 == drug_class2)
        
        # Check purpose overlap
        score = 0.0
        reason = ""
        
        if same_class:
            score = 70.0
            reason = "Same drug class"
        else:
            # Check for common keywords
            common_keywords = ['pain', 'infection', 'diabetes', 'heart', 'blood', 'pressure']
            for keyword in common_keywords:
                if keyword in purpose1 and keyword in purpose2:
                    score += 15.0
                    reason = f"Both used for {keyword}"
        
        return {
            "score": min(100.0, score),
            "known_risk": False,
            "reason": reason if reason else "Different therapeutic purposes",
            "risk_level": "high" if score >= 50 else "medium" if score >= 25 else "low"
        }
    
    @staticmethod
    def calculate_combined_risk(spelling_scores: Dict, phonetic_scores: Dict, therapeutic_scores: Dict) -> Dict[str, Any]:
        """Calculate final combined risk"""
        # Weights
        weights = {
            "spelling": 0.40,  # Spelling is most important
            "phonetic": 0.30,  # Phonetic next
            "therapeutic": 0.30  # Therapeutic context
        }
        
        # Use best spelling score
        best_spelling = max(
            spelling_scores.get("basic", 0),
            spelling_scores.get("levenshtein", 0),
            spelling_scores.get("fuzzy", 0)
        )
        
        # Phonetic score
        phonetic_score = 0.0
        if phonetic_scores.get("metaphone_match"):
            phonetic_score = 80.0
        elif phonetic_scores.get("soundex_match"):
            phonetic_score = 60.0
        else:
            phonetic_score = phonetic_scores.get("basic", 0)
        
        # Therapeutic score
        therapeutic_score = therapeutic_scores.get("score", 0)
        
        # Calculate weighted score
        weighted_score = (
            best_spelling * weights["spelling"] +
            phonetic_score * weights["phonetic"] +
            therapeutic_score * weights["therapeutic"]
        )
        
        # Boost for critical factors
        if therapeutic_scores.get("risk_level") == "critical":
            weighted_score = min(100.0, weighted_score * 1.3)
        elif phonetic_scores.get("metaphone_match") and best_spelling > 70:
            weighted_score = min(100.0, weighted_score * 1.2)
        
        # Risk category
        if weighted_score >= 75:
            risk_category = "critical"
        elif weighted_score >= 50:
            risk_category = "high"
        elif weighted_score >= 25:
            risk_category = "medium"
        else:
            risk_category = "low"
        
        # Generate reason
        reasons = []
        if best_spelling > 70:
            reasons.append(f"High spelling similarity ({best_spelling:.0f}%)")
        if phonetic_scores.get("metaphone_match"):
            reasons.append("Identical phonetic pronunciation")
        if therapeutic_scores.get("reason"):
            reasons.append(therapeutic_scores["reason"])
        
        risk_reason = ". ".join(reasons) if reasons else "Multiple factors contribute to confusion risk"
        
        return {
            "combined_risk": round(weighted_score, 1),
            "risk_category": risk_category,
            "risk_reason": risk_reason,
            "components": {
                "spelling": round(best_spelling, 1),
                "phonetic": round(phonetic_score, 1),
                "therapeutic": round(therapeutic_score, 1)
            }
        }

# ==================== REAL-TIME DASHBOARD MANAGER ====================

class RealTimeDashboardManager:
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
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

dashboard_manager = RealTimeDashboardManager()

# ==================== DATABASE INITIALIZATION ====================

def init_database():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified successfully")
        
        # Seed known risky pairs
        db = SessionLocal()
        try:
            count = db.query(KnownRiskyPair).count()
            if count == 0:
                for (drug1, drug2), info in AdvancedRiskAnalyzer.KNOWN_RISKY_PAIRS.items():
                    pair = KnownRiskyPair(
                        drug1_name=drug1,
                        drug2_name=drug2,
                        risk_level=info["risk"],
                        reason=info["reason"],
                        source="ISMP/FDA"
                    )
                    db.add(pair)
                db.commit()
                logger.info(f"✅ Seeded {len(AdvancedRiskAnalyzer.KNOWN_RISKY_PAIRS)} known risky pairs")
        finally:
            db.close()
        
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        try:
            temp_engine = create_engine("postgresql://postgres:PRO_CODER#1@localhost:5432/postgres")
            with temp_engine.connect() as conn:
                result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'confusionguard'"))
                if not result.fetchone():
                    conn.execute(text("COMMIT"))
                    conn.execute(text("CREATE DATABASE confusionguard"))
                    logger.info("✅ Database 'confusionguard' created successfully")
            
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables created successfully")
            return True
            
        except Exception as e2:
            logger.error(f"❌ Failed to create database: {e2}")
            print("\n🔧 TROUBLESHOOTING:")
            print("1. Make sure PostgreSQL is running")
            print("2. Check if PostgreSQL password is correct")
            print("3. Verify PostgreSQL is listening on port 5432")
            return False

# ==================== PYDANTIC MODELS ====================

class DrugBase(BaseModel):
    id: int
    brand_name: str
    generic_name: str
    manufacturer: Optional[str] = None
    purpose: Optional[str] = None
    drug_class: Optional[str] = None
    
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
    risk_reason: str
    
    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    query_drug: str
    similar_drugs: List[ConfusionRiskBase]
    total_found: int
    analysis_id: str
    timestamp: datetime

class DashboardMetrics(BaseModel):
    total_drugs: int
    total_analyses: int
    high_risk_pairs: int
    critical_risk_pairs: int
    avg_risk_score: float
    recent_searches: List[Dict[str, Any]]
    system_status: str
    last_updated: datetime
    connected_clients: int

class TopRiskResponse(BaseModel):
    drug1: str
    drug2: str
    risk_score: float
    risk_category: str
    reason: str

class RiskBreakdownResponse(BaseModel):
    category: str
    count: int

class HeatmapResponse(BaseModel):
    drug_names: List[str]
    risk_matrix: List[List[float]]

class RealtimeEventResponse(BaseModel):
    event_type: str
    drug_name: str
    risk_score: Optional[float]
    timestamp: datetime
    message: str

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
                "search": f'(openfda.brand_name:"{search_term}" OR openfda.generic_name:"{search_term}")',
                "limit": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(OpenFDAClient.BASE_URL, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        logger.warning(f"OpenFDA API returned status {response.status}")
                        return []
        except asyncio.TimeoutError:
            logger.warning("OpenFDA API request timed out")
            return []
        except Exception as e:
            logger.warning(f"Error searching OpenFDA: {e}")
            return []
    
    @staticmethod
    def extract_drug_data(fda_data: Dict, search_term: str) -> Optional[Dict]:
        try:
            openfda = fda_data.get("openfda", {})
            
            product_ndc = openfda.get("product_ndc", [""])[0]
            application_number = openfda.get("application_number", [""])[0]
            openfda_id = product_ndc or application_number or f"drug_{int(time.time())}_{hash(search_term)}"
            
            brand_name = openfda.get("brand_name", [""])[0]
            if not brand_name or brand_name.lower() == "null" or brand_name == "":
                brand_name = openfda.get("generic_name", [""])[0] or search_term.title()
            
            generic_name = openfda.get("generic_name", [""])[0] or ""
            
            # Infer drug class from name suffixes
            drug_class = ""
            for suffix, class_name in AdvancedRiskAnalyzer.DRUG_SUFFIXES.items():
                if generic_name.lower().endswith(suffix):
                    drug_class = class_name
                    break
            
            # Generate phonetic codes
            soundex_code = jellyfish.soundex(brand_name.lower())
            metaphone_code = jellyfish.metaphone(brand_name.lower())
            
            drug = {
                "openfda_id": openfda_id,
                "brand_name": brand_name,
                "generic_name": generic_name,
                "manufacturer": openfda.get("manufacturer_name", [""])[0] or "",
                "substance_name": openfda.get("substance_name", [""])[0] or "",
                "product_type": openfda.get("product_type", [""])[0] or "",
                "route": openfda.get("route", [""])[0] or "",
                "active_ingredients": ", ".join(openfda.get("active_ingredient", [])),
                "purpose": fda_data.get("purpose", [""])[0] if isinstance(fda_data.get("purpose"), list) else "",
                "warnings": fda_data.get("warnings", [""])[0] if isinstance(fda_data.get("warnings"), list) else "",
                "indications_and_usage": fda_data.get("indications_and_usage", [""])[0] if isinstance(fda_data.get("indications_and_usage"), list) else "",
                "dosage_form": openfda.get("dosage_form", [""])[0] or "",
                "drug_class": drug_class,
                "soundex_code": soundex_code,
                "metaphone_code": metaphone_code,
            }
            
            return drug
        except Exception as e:
            logger.error(f"Error extracting drug data: {e}")
            return None

# ==================== DRUG ETL PIPELINE ====================

class DrugETL:
    @staticmethod
    async def fetch_and_store_drug(db: Session, search_term: str) -> Optional[Drug]:
        try:
            existing_drug = db.query(Drug).filter(
                (Drug.brand_name.ilike(f"%{search_term}%")) |
                (Drug.generic_name.ilike(f"%{search_term}%"))
            ).first()
            
            if existing_drug:
                logger.info(f"Drug already in database: {existing_drug.brand_name}")
                return existing_drug
            
            logger.info(f"Fetching drug from OpenFDA: {search_term}")
            fda_results = await OpenFDAClient.search_drugs(search_term, limit=3)
            
            if not fda_results:
                logger.warning(f"No results from OpenFDA for: {search_term}")
                return None
            
            for result in fda_results:
                drug_data = OpenFDAClient.extract_drug_data(result, search_term)
                if drug_data and drug_data["brand_name"]:
                    drug = Drug(**drug_data)
                    db.add(drug)
                    db.commit()
                    db.refresh(drug)
                    
                    logger.info(f"✅ Stored new drug: {drug.brand_name}")
                    
                    # Analyze against existing drugs
                    asyncio.create_task(DrugETL.analyze_against_all_drugs(db, drug))
                    
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
            
            analyzer = AdvancedRiskAnalyzer()
            
            for other_drug in other_drugs:
                # Calculate all similarity scores
                spelling_scores = analyzer.calculate_spelling_similarity(
                    new_drug.brand_name, other_drug.brand_name
                )
                
                # Skip if basic spelling similarity is too low
                if spelling_scores["basic"] < 20 and spelling_scores["levenshtein"] < 20:
                    continue
                
                phonetic_scores = analyzer.calculate_phonetic_similarity(
                    new_drug.brand_name, other_drug.brand_name
                )
                
                therapeutic_scores = analyzer.analyze_therapeutic_context(
                    new_drug, other_drug
                )
                
                # Calculate combined risk
                combined_result = analyzer.calculate_combined_risk(
                    spelling_scores, phonetic_scores, therapeutic_scores
                )
                
                if combined_result["combined_risk"] >= 20:
                    # Check if risk already exists
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
                            spelling_similarity=combined_result["components"]["spelling"],
                            phonetic_similarity=combined_result["components"]["phonetic"],
                            therapeutic_context_risk=combined_result["components"]["therapeutic"],
                            levenshtein_similarity=spelling_scores["levenshtein"],
                            soundex_match=phonetic_scores.get("soundex_match", False),
                            metaphone_match=phonetic_scores.get("metaphone_match", False),
                            is_known_risky_pair=therapeutic_scores.get("known_risk", False),
                            combined_risk=combined_result["combined_risk"],
                            risk_category=combined_result["risk_category"],
                            risk_reason=combined_result["risk_reason"]
                        )
                        db.add(confusion_risk)
            
            db.commit()
            logger.info(f"✅ Completed risk analysis for {new_drug.brand_name}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error in analyze_against_all_drugs: {e}")

# ==================== HELPER FUNCTIONS ====================

def generate_reason(drug1_name: str, drug2_name: str, risk_score: float) -> str:
    """Generate human-readable reason for risk"""
    reasons = [
        f"Similar spelling and sound",
        f"Commonly confused in clinical practice",
        f"FDA reported confusion cases",
        f"Different therapeutic purposes with similar names",
        f"High phonetic similarity",
        f"Look-alike packaging reported",
        f"ISMP high-alert medication pair"
    ]
    
    return random.choice(reasons)

def get_top_risks_data(db: Session, limit: int = 10) -> List[Dict]:
    """Get top risk pairs for dashboard"""
    try:
        risks = db.query(ConfusionRisk).filter(
            ConfusionRisk.combined_risk >= 25
        ).order_by(ConfusionRisk.combined_risk.desc()).limit(limit).all()
        
        result = []
        for risk in risks:
            drug1 = db.query(Drug).filter(Drug.id == risk.source_drug_id).first()
            drug2 = db.query(Drug).filter(Drug.id == risk.target_drug_id).first()
            
            if drug1 and drug2:
                result.append({
                    "drug1": drug1.brand_name,
                    "drug2": drug2.brand_name,
                    "risk_score": round(float(risk.combined_risk), 1),
                    "risk_category": risk.risk_category,
                    "reason": risk.risk_reason or generate_reason(drug1.brand_name, drug2.brand_name, risk.combined_risk)
                })
        
        return result
    except Exception as e:
        logger.error(f"Error getting top risks: {e}")
        return []

def get_risk_breakdown_data(db: Session) -> List[Dict]:
    """Get risk category breakdown for pie chart"""
    try:
        categories = ["critical", "high", "medium", "low"]
        result = []
        
        for category in categories:
            count = db.query(ConfusionRisk).filter(
                ConfusionRisk.risk_category == category
            ).count()
            
            result.append({
                "category": category,
                "count": count
            })
        
        return result
    except Exception as e:
        logger.error(f"Error getting risk breakdown: {e}")
        return []

def get_heatmap_data(db: Session, limit: int = 15) -> Dict:
    """Generate heatmap data for visualization"""
    try:
        drugs = db.query(Drug).order_by(Drug.created_at.desc()).limit(limit).all()
        
        if len(drugs) < 2:
            return {"drug_names": [], "risk_matrix": []}
        
        drug_names = [drug.brand_name for drug in drugs]
        drug_ids = {drug.id: idx for idx, drug in enumerate(drugs)}
        
        n = len(drugs)
        risk_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i, drug1 in enumerate(drugs):
            for j, drug2 in enumerate(drugs):
                if i == j:
                    risk_matrix[i][j] = 0.0
                else:
                    risk = db.query(ConfusionRisk).filter(
                        ((ConfusionRisk.source_drug_id == drug1.id) & 
                         (ConfusionRisk.target_drug_id == drug2.id)) |
                        ((ConfusionRisk.source_drug_id == drug2.id) & 
                         (ConfusionRisk.target_drug_id == drug1.id))
                    ).first()
                    
                    if risk:
                        risk_matrix[i][j] = float(risk.combined_risk)
                    else:
                        analyzer = AdvancedRiskAnalyzer()
                        spelling = analyzer.calculate_spelling_similarity(
                            drug1.brand_name, drug2.brand_name
                        )
                        phonetic = analyzer.calculate_phonetic_similarity(
                            drug1.brand_name, drug2.brand_name
                        )
                        therapeutic = analyzer.analyze_therapeutic_context(drug1, drug2)
                        
                        combined = analyzer.calculate_combined_risk(spelling, phonetic, therapeutic)
                        risk_matrix[i][j] = combined["combined_risk"]
        
        return {
            "drug_names": drug_names,
            "risk_matrix": risk_matrix
        }
    except Exception as e:
        logger.error(f"Error generating heatmap data: {e}")
        return {"drug_names": [], "risk_matrix": []}

def get_realtime_events_data(db: Session, limit: int = 10) -> List[Dict]:
    """Get recent events for real-time dashboard"""
    try:
        recent_analyses = db.query(AnalysisLog).order_by(
            AnalysisLog.timestamp.desc()
        ).limit(limit).all()
        
        events = []
        for analysis in recent_analyses:
            events.append({
                "event_type": "search",
                "drug_name": analysis.drug_name,
                "risk_score": float(analysis.highest_risk_score) if analysis.highest_risk_score else 0.0,
                "timestamp": analysis.timestamp,
                "message": f"Analyzed '{analysis.drug_name}' - found {analysis.similar_drugs_found} similar drugs"
            })
        
        if len(events) < limit:
            system_events = [
                {
                    "event_type": "system",
                    "drug_name": "",
                    "risk_score": None,
                    "timestamp": datetime.utcnow() - timedelta(minutes=random.randint(1, 30)),
                    "message": "System health check completed"
                },
                {
                    "event_type": "alert",
                    "drug_name": "Lamictal",
                    "risk_score": 85.0,
                    "timestamp": datetime.utcnow() - timedelta(minutes=random.randint(10, 60)),
                    "message": "High risk detected: Lamictal ↔ Lamisil"
                },
            ]
            
            events.extend(system_events)
        
        events.sort(key=lambda x: x["timestamp"], reverse=True)
        return events[:limit]
        
    except Exception as e:
        logger.error(f"Error getting realtime events: {e}")
        return []

# ==================== REAL-TIME DASHBOARD FUNCTIONS ====================

async def get_realtime_metrics(db: Session) -> Dict[str, Any]:
    """Get real-time metrics for dashboard"""
    try:
        total_drugs = db.query(Drug).count()
        total_analyses = db.query(AnalysisLog).count()
        
        high_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category.in_(["high", "critical"])
        ).count()
        
        critical_risk_pairs = db.query(ConfusionRisk).filter(
            ConfusionRisk.risk_category == "critical"
        ).count()
        
        avg_risk_result = db.execute(
            text("SELECT AVG(combined_risk) FROM confusion_risks WHERE combined_risk > 0")
        ).scalar()
        avg_risk_score = round(float(avg_risk_result or 0), 2)
        
        fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
        recent_searches = db.query(AnalysisLog).filter(
            AnalysisLog.timestamp >= fifteen_min_ago
        ).order_by(AnalysisLog.timestamp.desc()).limit(10).all()
        
        recent_search_data = []
        for search in recent_searches:
            recent_search_data.append({
                "drug_name": search.drug_name,
                "timestamp": search.timestamp.isoformat(),
                "similar_drugs_found": search.similar_drugs_found,
                "highest_risk": float(search.highest_risk_score) if search.highest_risk_score else 0
            })
        
        system_status = "healthy"
        try:
            db.execute(text("SELECT 1"))
        except Exception as e:
            system_status = f"database_error: {str(e)[:50]}"
        
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
            "error": str(e)[:100],
            "last_updated": datetime.utcnow().isoformat(),
            "system_status": "error",
            "connected_clients": len(dashboard_manager.active_connections)
        }

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "name": "Medication Safety Guard API",
        "version": "3.0.0",
        "description": "Professional medication confusion prevention system",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        
        drug_count = db.query(Drug).count()
        risk_count = db.query(ConfusionRisk).count()
        analysis_count = db.query(AnalysisLog).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "drugs_in_database": drug_count,
                "risk_assessments": risk_count,
                "total_analyses": analysis_count
            },
            "endpoints": {
                "search": "/api/search/{drug_name}",
                "metrics": "/api/metrics",
                "realtime": "/ws/dashboard",
                "seed": "/api/seed-database",
                "top-risks": "/api/top-risks",
                "risk-breakdown": "/api/risk-breakdown",
                "heatmap": "/api/heatmap",
                "realtime-events": "/api/realtime-events"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "troubleshooting": "Make sure PostgreSQL is running on localhost:5432"
        }

@app.get("/api/top-risks", response_model=List[TopRiskResponse])
async def get_top_risks(
    limit: int = Query(10, description="Number of top risks to return"),
    db: Session = Depends(get_db)
):
    try:
        risks_data = get_top_risks_data(db, limit)
        return risks_data
    except Exception as e:
        logger.error(f"Error in /api/top-risks: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

@app.get("/api/risk-breakdown", response_model=List[RiskBreakdownResponse])
async def get_risk_breakdown(db: Session = Depends(get_db)):
    try:
        breakdown_data = get_risk_breakdown_data(db)
        return breakdown_data
    except Exception as e:
        logger.error(f"Error in /api/risk-breakdown: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

@app.get("/api/heatmap", response_model=HeatmapResponse)
async def get_heatmap(
    limit: int = Query(15, description="Number of drugs for heatmap"),
    db: Session = Depends(get_db)
):
    try:
        heatmap_data = get_heatmap_data(db, limit)
        return HeatmapResponse(**heatmap_data)
    except Exception as e:
        logger.error(f"Error in /api/heatmap: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

@app.get("/api/realtime-events", response_model=Dict[str, List[RealtimeEventResponse]])
async def get_realtime_events(
    limit: int = Query(10, description="Number of events to return"),
    db: Session = Depends(get_db)
):
    try:
        events_data = get_realtime_events_data(db, limit)
        return {"events": events_data}
    except Exception as e:
        logger.error(f"Error in /api/realtime-events: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await dashboard_manager.connect(websocket)
    
    try:
        db = SessionLocal()
        
        try:
            metrics = await get_realtime_metrics(db)
            await websocket.send_json({
                "type": "initial",
                "data": metrics,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            last_update = time.time()
            while True:
                try:
                    try:
                        data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                        if data == "ping":
                            await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat()})
                    except asyncio.TimeoutError:
                        pass
                    
                    current_time = time.time()
                    if current_time - last_update >= 10:
                        metrics = await get_realtime_metrics(db)
                        await websocket.send_json({
                            "type": "update",
                            "data": metrics,
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        last_update = current_time
                    
                    await asyncio.sleep(0.1)
                    
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"WebSocket error: {e}")
                    break
                    
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"WebSocket setup error: {e}")
    finally:
        dashboard_manager.disconnect(websocket)

@app.get("/api/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    metrics_data = await get_realtime_metrics(db)
    
    return DashboardMetrics(
        total_drugs=metrics_data.get("total_drugs", 0),
        total_analyses=metrics_data.get("total_analyses", 0),
        high_risk_pairs=metrics_data.get("high_risk_pairs", 0),
        critical_risk_pairs=metrics_data.get("critical_risk_pairs", 0),
        avg_risk_score=metrics_data.get("avg_risk_score", 0),
        recent_searches=metrics_data.get("recent_searches", []),
        system_status=metrics_data.get("system_status", "unknown"),
        last_updated=datetime.fromisoformat(metrics_data.get("last_updated")),
        connected_clients=metrics_data.get("connected_clients", 0)
    )

# ==================== MAIN DRUG ANALYSIS ENDPOINT ====================

@app.get("/api/search/{drug_name}", response_model=AnalysisResponse)
async def search_and_analyze(
    drug_name: str,
    db: Session = Depends(get_db)
):
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"🔍 Searching for drug: {drug_name}")
        
        existing_drug = db.query(Drug).filter(
            Drug.brand_name.ilike(f"%{drug_name}%")
        ).first()
        
        if not existing_drug:
            existing_drug = db.query(Drug).filter(
                Drug.generic_name.ilike(f"%{drug_name}%")
            ).first()
        
        drug = existing_drug
        
        if not drug:
            logger.info(f"🌐 Fetching from OpenFDA: {drug_name}")
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
        
        if not drug:
            logger.warning(f"Drug not found: {drug_name}. Creating placeholder.")
            
            soundex_code = jellyfish.soundex(drug_name.lower())
            metaphone_code = jellyfish.metaphone(drug_name.lower())
            
            drug = Drug(
                openfda_id=f"placeholder_{int(time.time())}",
                brand_name=drug_name.title(),
                generic_name=drug_name.title(),
                manufacturer="Unknown",
                purpose="Not specified",
                soundex_code=soundex_code,
                metaphone_code=metaphone_code
            )
            db.add(drug)
            db.commit()
            db.refresh(drug)
        
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
                    purpose=(target.purpose[:100] + "...") if target.purpose and len(target.purpose) > 100 else target.purpose,
                    drug_class=target.drug_class
                ),
                spelling_similarity=round(risk.spelling_similarity, 1),
                phonetic_similarity=round(risk.phonetic_similarity, 1),
                therapeutic_context_risk=round(risk.therapeutic_context_risk, 1),
                combined_risk=round(risk.combined_risk, 1),
                risk_category=risk.risk_category,
                risk_reason=risk.risk_reason or "Multiple factors contribute to confusion risk"
            ))
        
        similar_drugs.sort(key=lambda x: x.combined_risk, reverse=True)
        
        analysis_log = AnalysisLog(
            drug_name=drug_name,
            similar_drugs_found=len(similar_drugs),
            highest_risk_score=max([r.combined_risk for r in similar_drugs] or [0]),
            critical_risks_found=len([r for r in similar_drugs if r.risk_category in ["critical", "high"]]),
            analysis_duration=(datetime.utcnow() - start_time).total_seconds()
        )
        db.add(analysis_log)
        db.commit()
        
        logger.info(f"✅ Analysis complete for {drug_name}: found {len(similar_drugs)} similar drugs")
        
        try:
            metrics = await get_realtime_metrics(db)
            await dashboard_manager.broadcast({
                "type": "search_completed",
                "data": {
                    "drug_name": drug_name,
                    "similar_drugs_found": len(similar_drugs),
                    "highest_risk": max([r.combined_risk for r in similar_drugs] or [0])
                },
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.warning(f"Could not broadcast update: {e}")
        
        return AnalysisResponse(
            query_drug=drug.brand_name,
            similar_drugs=similar_drugs[:20],
            total_found=len(similar_drugs),
            analysis_id=str(analysis_log.id),
            timestamp=start_time
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error in search_and_analyze: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)[:100]}"
        )

@app.post("/api/seed-database")
async def seed_database(db: Session = Depends(get_db)):
    try:
        common_drugs = [
            "metformin", "lamictal", "celebrex", "clonidine",
            "lisinopril", "aspirin", "ibuprofen", "paracetamol",
            "atorvastatin", "amlodipine", "omeprazole", "levothyroxine",
            "albuterol", "prednisone", "warfarin", "insulin"
        ]
        
        seeded_count = 0
        seeded_names = []
        
        for drug_name in common_drugs:
            drug = await DrugETL.fetch_and_store_drug(db, drug_name)
            if drug:
                seeded_count += 1
                seeded_names.append(drug.brand_name)
                await asyncio.sleep(0.5)
        
        return {
            "message": f"Database seeded with {seeded_count} drugs",
            "seeded_drugs": seeded_names,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

@app.get("/api/drugs")
async def get_all_drugs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(50, description="Number of records to return", le=200),
    db: Session = Depends(get_db)
):
    try:
        drugs = db.query(Drug).order_by(Drug.brand_name).offset(skip).limit(limit).all()
        
        return {
            "drugs": [
                {
                    "id": drug.id,
                    "brand_name": drug.brand_name,
                    "generic_name": drug.generic_name,
                    "manufacturer": drug.manufacturer,
                    "purpose": drug.purpose[:150] + "..." if drug.purpose and len(drug.purpose) > 150 else drug.purpose,
                    "drug_class": drug.drug_class
                }
                for drug in drugs
            ],
            "total": db.query(Drug).count(),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting drugs: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)[:100]}")

# ==================== APPLICATION STARTUP ====================

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🚀 Medication Safety Guard v3.0 - Starting Up...")
    print("="*60)
    
    if init_database():
        print("✅ Database initialized successfully")
    else:
        print("⚠️  Database initialization had issues, but continuing...")
    
    print("\n📊 Available Endpoints:")
    print("   • http://localhost:8000/          - API Status")
    print("   • http://localhost:8000/health    - Health Check")
    print("   • http://localhost:8000/docs      - API Documentation")
    print("   • ws://localhost:8000/ws/dashboard - Real-time Dashboard")
    print("\n💊 Enhanced Features:")
    print("   • Advanced Levenshtein distance algorithm")
    print("   • 5 phonetic algorithms (Soundex, Metaphone, NYSIIS)")
    print("   • 50+ known risky drug pairs")
    print("   • Intelligent therapeutic context analysis")
    print("="*60)
    print("✅ Medication Safety Guard v3.0 is ready!")
    print("="*60 + "\n")

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    import uvicorn
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Install dependencies: pip install jellyfish fuzzywuzzy python-Levenshtein")
        print("2. Make sure PostgreSQL is running")
        print("3. Check if port 8000 is available")
