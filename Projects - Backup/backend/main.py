from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
from typing import List
import json
import plotly.graph_objects as go
import plotly.utils
from database import save_prediction, get_prediction_history

# Initialize FastAPI
app = FastAPI(title="Thyroid Disease Prediction API", version="1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and features
print("🔄 Loading Thyroid Model...")
try:
    with open("ml_models/thyroid_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Load features list
try:
    with open("ml_models/features.txt", "r") as f:
        FEATURES = [line.strip() for line in f.readlines()]
    print(f"✅ Features loaded: {len(FEATURES)} features")
except:
    # Default features based on your list
    FEATURES = ['Age', 'Family_History', 'Radiation_Exposure', 'Iodine_Deficiency',
                'Smoking', 'Obesity', 'Diabetes', 'TSH_Level', 'T3_Level', 'T4_Level',
                'Nodule_Size', 'Thyroid_Cancer_Risk', 'Gender_Male']

# Pydantic Model for Input Validation
class ThyroidData(BaseModel):
    Age: float
    Family_History: int
    Radiation_Exposure: int
    Iodine_Deficiency: int
    Smoking: int
    Obesity: int
    Diabetes: int
    TSH_Level: float
    T3_Level: float
    T4_Level: float
    Nodule_Size: float
    Thyroid_Cancer_Risk: int
    Gender_Male: int

class PredictionResponse(BaseModel):
    prediction: str
    risk_percentage: float
    confidence: str
    features_importance: dict
    chart_data: str  # JSON string of Plotly chart

# Helper Functions
def calculate_risk_percentage(prediction_prob):
    """Convert probability to risk percentage"""
    risk = prediction_prob * 100
    return round(risk, 2)

def get_confidence_level(risk_percentage):
    """Determine confidence level based on risk"""
    if risk_percentage >= 70:
        return "High"
    elif risk_percentage >= 40:
        return "Moderate"
    else:
        return "Low"

def create_risk_chart(risk_percentage):
    """Create Plotly gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Thyroid Cancer Risk", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_percentage
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(t=0, b=0))
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_feature_importance():
    """Get feature importance from model"""
    if hasattr(model, 'coef_'):
        importance = abs(model.coef_[0])
        features_dict = {feature: round(float(imp), 4) for feature, imp in zip(FEATURES, importance)}
        return dict(sorted(features_dict.items(), key=lambda x: x[1], reverse=True)[:5])
    return {feature: 0.1 for feature in FEATURES[:5]}

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Thyroid Disease Prediction API", "status": "active"}

@app.get("/features")
def get_features():
    """Get list of required features"""
    return {"features": FEATURES, "count": len(FEATURES)}

@app.post("/predict", response_model=PredictionResponse)
def predict_thyroid(data: ThyroidData):
    """Make thyroid disease prediction"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert input to DataFrame with correct feature order
        input_data = {feature: getattr(data, feature) for feature in FEATURES}
        df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction_prob = model.predict_proba(df)[0][1]  # Probability of class 1 (Malignant)
        prediction_class = model.predict(df)[0]
        
        # Calculate risk percentage
        risk_percentage = calculate_risk_percentage(prediction_prob)
        
        # Determine prediction result
        prediction_result = "Malignant" if prediction_class == 1 else "Benign"
        
        # Get confidence level
        confidence = get_confidence_level(risk_percentage)
        
        # Get top important features
        features_importance = get_feature_importance()
        
        # Create visualization chart
        chart_data = create_risk_chart(risk_percentage)
        
        # Save to database
        save_prediction(input_data, prediction_result, risk_percentage)
        
        return {
            "prediction": prediction_result,
            "risk_percentage": risk_percentage,
            "confidence": confidence,
            "features_importance": features_importance,
            "chart_data": chart_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/history")
def get_history(limit: int = 10):
    """Get prediction history"""
    try:
        history = get_prediction_history(limit)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features_count": len(FEATURES)
    }

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)