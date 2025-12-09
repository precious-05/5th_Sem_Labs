from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import pickle
import numpy as np
import pandas as pd
from typing import List, Dict
import json
import plotly.graph_objects as go
import plotly.utils
from database import save_prediction, get_prediction_history


#------------------INITIAZLIZING THE FAST-API------------------------
app = FastAPI(title="Thyroid Disease Prediction API", version="1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Load model and features
print("Loading Thyroid Model...")
try:
    with open("ml_models/thyroid_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load features list
try:
    with open("ml_models/features.txt", "r") as f:
        FEATURES = [line.strip() for line in f.readlines()]
    print(f"Features loaded: {len(FEATURES)} features")
except:
    FEATURES = ['Age', 'Family_History', 'Radiation_Exposure', 'Iodine_Deficiency',
                'Smoking', 'Obesity', 'Diabetes', 'TSH_Level', 'T3_Level', 'T4_Level',
                'Nodule_Size', 'Thyroid_Cancer_Risk', 'Gender_Male']

# ✅ FIXED: Correct Data Types based on your dataset
class ThyroidData(BaseModel):
    Age: int  # ✅ Changed from float to int
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
    Gender_Male: float  # ✅ Changed from int to float
    
    # ✅ Added validation (optional but recommended)
    @validator('Age')
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120')
        return v
    
    @validator('Gender_Male')
    def validate_gender(cls, v):
        # Accept both int (0/1) and float (0.0/1.0)
        if v not in [0, 1, 0.0, 1.0]:
            raise ValueError('Gender_Male must be 0 or 1')
        return float(v)  # Convert to float for consistency

class PredictionResponse(BaseModel):
    prediction: str
    risk_percentage: float
    confidence: str
    features_importance: Dict[str, float]  # ✅ Better type hint
    chart_data: str

# Helper Functions (Only necessary fixes)
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

# API Endpoints (No changes needed)
@app.get("/")
def read_root():
    return {"message": "Thyroid Disease Prediction API", "status": "active"}

@app.get("/features")
def get_features():
    return {"features": FEATURES, "count": len(FEATURES)}

@app.post("/predict", response_model=PredictionResponse)
def predict_thyroid(data: ThyroidData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # ✅ Ensure Gender_Male is float (frontend compatibility)
        input_dict = data.dict()
        input_dict['Gender_Male'] = float(input_dict['Gender_Male'])
        
        # Convert input to DataFrame
        df = pd.DataFrame([input_dict])
        
        # Make prediction
        prediction_prob = model.predict_proba(df)[0][1]
        prediction_class = model.predict(df)[0]
        
        risk_percentage = calculate_risk_percentage(prediction_prob)
        prediction_result = "Malignant" if prediction_class == 1 else "Benign"
        confidence = get_confidence_level(risk_percentage)
        features_importance = get_feature_importance()
        chart_data = create_risk_chart(risk_percentage)
        
        # Save to database
        save_prediction(input_dict, prediction_result, risk_percentage)
        
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
    try:
        history = get_prediction_history(limit)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features_count": len(FEATURES)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)