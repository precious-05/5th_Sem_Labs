"""
BACKEND - Day 2 Simplified Version
Matching your frontend code exactly
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="MediNomix API",
    description="Medication Safety Backend",
    version="2.0"
)

# Add CORS middleware - CRITICAL for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# ========== DATABASE (Simulated) ==========
fake_drugs_db = [
    {"id": 1, "name": "Metformin", "type": "Diabetes", "risk": 45},
    {"id": 2, "name": "Lamictal", "type": "Epilepsy", "risk": 85},
    {"id": 3, "name": "Aspirin", "type": "Pain Relief", "risk": 15},
]

# ========== API ENDPOINTS ==========

@app.get("/")
async def root():
    """Root endpoint - shows API is working"""
    return {
        "app": "MediNomix Backend",
        "version": "2.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "search": "/api/search/{drug_name}",
            "drugs": "/api/drugs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Backend is running properly"
    }

@app.get("/api/search/{drug_name}")
async def search_drug(drug_name: str):
    """Search for a drug - matches your frontend call"""
    
    print(f"🔍 Backend received request for: {drug_name}")
    
    # Simulate database search
    results = []
    for drug in fake_drugs_db:
        if drug_name.lower() in drug["name"].lower():
            results.append(drug)
    
    # Simulate finding similar drugs
    similar_drugs = []
    for drug in fake_drugs_db:
        if drug["name"].lower() != drug_name.lower():
            similar_drugs.append({
                "target_drug": drug,
                "similarity_score": drug["risk"],
                "risk_category": "high" if drug["risk"] > 50 else "medium" if drug["risk"] > 25 else "low"
            })
    
    print(f"✅ Backend sending response: {len(similar_drugs)} results")
    
    return {
        "query_drug": drug_name,
        "similar_drugs": similar_drugs[:5],  # Limit to 5 for simplicity
        "total_found": len(similar_drugs),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/drugs")
async def get_all_drugs():
    """Get all drugs - simple endpoint"""
    return {
        "drugs": fake_drugs_db,
        "count": len(fake_drugs_db),
        "timestamp": datetime.utcnow().isoformat()
    }

# Run the server
if __name__ == "__main__":
    print("🚀 Starting MediNomix Backend...")
    print("📡 API available at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,       # Same port your frontend expects
        log_level="info"
    )