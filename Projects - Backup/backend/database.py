from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["health_prediction_db"]
predictions_collection = db["thyroid_predictions"]

def save_prediction(user_data, prediction_result, risk_percentage):
    """Save prediction to MongoDB"""
    prediction_record = {
        "user_data": user_data,
        "prediction": prediction_result,
        "risk_percentage": risk_percentage,
        "timestamp": datetime.now(),
        "disease_type": "thyroid"
    }
    
    result = predictions_collection.insert_one(prediction_record)
    return str(result.inserted_id)

def get_prediction_history(limit=20):
    """Get recent predictions"""
    history = list(predictions_collection.find(
        {}, 
        {"_id": 0, "user_data": 1, "prediction": 1, "risk_percentage": 1, "timestamp": 1}
    ).sort("timestamp", -1).limit(limit))
    
    # Convert ObjectId to string and format timestamp
    for record in history:
        if "timestamp" in record:
            record["timestamp"] = record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    
    return history