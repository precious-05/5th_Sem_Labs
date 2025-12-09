"""
IMPROVED DATABASE MODULE - Maintains EXACT same function signatures
to ensure main.py compatibility
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, DuplicateKeyError
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import logging
from typing import Dict, List, Any, Optional
import uuid

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "health_prediction_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "thyroid_predictions")

# Connection with improved settings
client = None
db = None
predictions_collection = None

def initialize_database():
    """Initialize database connection with error handling"""
    global client, db, predictions_collection
    
    try:
        # Connection with timeout and retry settings
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=50,  # Connection pooling
            minPoolSize=10
        )
        
        # Test connection
        client.admin.command('ping')
        
        db = client[DB_NAME]
        predictions_collection = db[COLLECTION_NAME]
        
        # ✅ Create indexes for performance (only once)
        create_indexes()
        
        logger.info(f"✅ MongoDB connected successfully to {DB_NAME}.{COLLECTION_NAME}")
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        client = None
        return False
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        return False

def create_indexes():
    """Create necessary indexes for performance"""
    try:
        # Compound index for fast sorting and filtering
        predictions_collection.create_index([("timestamp", -1)])
        
        # Index for disease_type if you want filtering later
        predictions_collection.create_index([("disease_type", 1)])
        
        # Unique prediction ID for reference
        predictions_collection.create_index([("prediction_id", 1)], unique=True)
        
        logger.info("✅ Database indexes created successfully")
    except Exception as e:
        logger.warning(f"⚠️ Index creation failed (might already exist): {e}")

def anonymize_user_data(user_data: Dict) -> Dict:
    """Anonymize sensitive user data before saving"""
    # Create a copy to avoid modifying original
    anonymized = user_data.copy()
    
    # Remove or hash any potentially identifiable information
    # Currently your data doesn't have PII, but for future safety
    
    # Example: If you had email or name fields
    # if 'email' in anonymized:
    #     anonymized['email'] = hash(anonymized['email'])
    
    return anonymized

def validate_prediction_data(user_data: Dict, prediction_result: str, risk_percentage: float) -> bool:
    """Validate data before saving to database"""
    try:
        # Basic validation
        if not isinstance(user_data, dict):
            logger.error("User data must be a dictionary")
            return False
            
        if prediction_result not in ["Benign", "Malignant"]:
            logger.error(f"Invalid prediction result: {prediction_result}")
            return False
            
        if not (0 <= risk_percentage <= 100):
            logger.error(f"Invalid risk percentage: {risk_percentage}")
            return False
            
        # Validate required features exist
        required_features = ['Age', 'Family_History', 'Radiation_Exposure', 
                            'Iodine_Deficiency', 'Smoking', 'Obesity', 'Diabetes', 
                            'TSH_Level', 'T3_Level', 'T4_Level', 'Nodule_Size', 
                            'Thyroid_Cancer_Risk', 'Gender_Male']
        
        for feature in required_features:
            if feature not in user_data:
                logger.error(f"Missing required feature: {feature}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False

def save_prediction(user_data: Dict, prediction_result: str, risk_percentage: float) -> str:
    """
    Save prediction to MongoDB - EXACT SAME SIGNATURE as before
    Returns: prediction_id as string
    """
    global predictions_collection
    
    # Initialize if not already done
    if predictions_collection is None:
        if not initialize_database():
            logger.warning("⚠️ Database not available, prediction not saved")
            return "database_unavailable"
    
    try:
        # Validate input data
        if not validate_prediction_data(user_data, prediction_result, risk_percentage):
            logger.warning("Invalid prediction data, saving with warning")
            # Still save but with warning flag
        
        # Anonymize user data (for privacy)
        safe_user_data = anonymize_user_data(user_data)
        
        # Create prediction record with additional metadata
        prediction_record = {
            "prediction_id": str(uuid.uuid4()),  # Unique ID for reference
            "user_data": safe_user_data,
            "prediction": prediction_result,
            "risk_percentage": risk_percentage,
            "confidence": get_confidence_level(risk_percentage),  # Added for history
            "timestamp": datetime.now(timezone.utc),  # UTC timezone aware
            "disease_type": "thyroid",
            "version": "1.0",  # API version for tracking
            "saved_successfully": True
        }
        
        # Insert into database
        result = predictions_collection.insert_one(prediction_record)
        
        logger.info(f"✅ Prediction saved with ID: {prediction_record['prediction_id']}")
        return str(prediction_record['prediction_id'])
        
    except DuplicateKeyError:
        # Retry with new UUID if duplicate (very rare)
        logger.warning("Duplicate prediction ID, generating new one")
        return save_prediction(user_data, prediction_result, risk_percentage)
    except Exception as e:
        logger.error(f"❌ Failed to save prediction: {e}")
        return f"error_{datetime.now().timestamp()}"

def get_prediction_history(limit: int = 20) -> List[Dict]:
    """
    Get recent predictions - EXACT SAME SIGNATURE as before
    Returns: List of prediction records
    """
    global predictions_collection
    
    # Initialize if not already done
    if predictions_collection is None:
        if not initialize_database():
            logger.warning("⚠️ Database not available, returning empty history")
            return []
    
    try:
        # Get recent predictions with all fields except MongoDB _id
        cursor = predictions_collection.find(
            {"saved_successfully": True},  # Only successful saves
            {
                "_id": 0,  # Exclude MongoDB internal ID
                "prediction_id": 1,
                "user_data": 1,
                "prediction": 1,
                "risk_percentage": 1,
                "confidence": 1,
                "timestamp": 1,
                "version": 1
            }
        ).sort("timestamp", -1).limit(min(limit, 100))  # Cap at 100 for safety
        
        history = list(cursor)
        
        # Format timestamp for frontend
        for record in history:
            if "timestamp" in record and record["timestamp"]:
                # Convert UTC to local string
                record["timestamp"] = record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"✅ Retrieved {len(history)} predictions from history")
        return history
        
    except Exception as e:
        logger.error(f"❌ Failed to get prediction history: {e}")
        return []

def get_statistics() -> Dict[str, Any]:
    """Get statistics for charts (NEW FUNCTION - optional)"""
    if predictions_collection is None:
        initialize_database()
    
    try:
        # Total predictions count
        total = predictions_collection.count_documents({})
        
        # Malignant vs Benign counts
        malignant_count = predictions_collection.count_documents({"prediction": "Malignant"})
        benign_count = predictions_collection.count_documents({"prediction": "Benign"})
        
        # Risk distribution
        high_risk = predictions_collection.count_documents({"risk_percentage": {"$gte": 70}})
        medium_risk = predictions_collection.count_documents({
            "risk_percentage": {"$gte": 40, "$lt": 70}
        })
        low_risk = predictions_collection.count_documents({"risk_percentage": {"$lt": 40}})
        
        # Average risk percentage
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_risk": {"$avg": "$risk_percentage"},
                "min_risk": {"$min": "$risk_percentage"},
                "max_risk": {"$max": "$risk_percentage"}
            }}
        ]
        
        stats_result = list(predictions_collection.aggregate(pipeline))
        stats = stats_result[0] if stats_result else {
            "avg_risk": 0, "min_risk": 0, "max_risk": 0
        }
        
        return {
            "total_predictions": total,
            "malignant_count": malignant_count,
            "benign_count": benign_count,
            "risk_distribution": {
                "high": high_risk,
                "medium": medium_risk,
                "low": low_risk
            },
            "risk_stats": {
                "average": round(stats.get("avg_risk", 0), 2),
                "minimum": round(stats.get("min_risk", 0), 2),
                "maximum": round(stats.get("max_risk", 0), 2)
            },
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get statistics: {e}")
        return {"error": "Unable to fetch statistics"}

def cleanup_old_records(days_to_keep: int = 90):
    """Cleanup old records (for maintenance)"""
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
        result = predictions_collection.delete_many({
            "timestamp": {"$lt": cutoff_date}
        })
        logger.info(f"✅ Cleaned up {result.deleted_count} old records")
        return result.deleted_count
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")
        return 0

# Helper function (same as in main.py for consistency)
def get_confidence_level(risk_percentage: float) -> str:
    """Determine confidence level based on risk"""
    if risk_percentage >= 70:
        return "High"
    elif risk_percentage >= 40:
        return "Moderate"
    else:
        return "Low"

# Initialize database on import
try:
    initialize_database()
except Exception as e:
    logger.warning(f"⚠️ Database initialization deferred: {e}")