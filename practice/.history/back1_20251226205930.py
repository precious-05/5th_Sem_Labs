from fastapi import FastAPI
# Ye line kehti hai: fastapi package se FastAPI class ko import kar lo apne program mein
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware



# app = FastAPI ()  # Is trh simply bhi likh skty hn lkn jo nichy title etc pass kia ha constructor mn wo optional ha but documenattion k ly acha ha
app = FastAPI(
    title= "MediNomix API",
    description= "Medication Safety backend",
    version= "2.0"  
)
# app FastAPI class ka ek instance (object) hai, jiske through hum apni web application ko define aur chalate hain
# FastAPI server ka ek instance (app) banya ha yhan jo backend web server ki tarah kaam karta hai
# Lekin ye sirf server ka "app object" banata hai, jo:
# Requests receive karne ke liye ready hota hai,
# Aur hmary defined routes (URLs) ko handle karta hai
# Lekin real server chalane ke liye hme is app ko run karna hota hai, jaise:
# uvicorn main:app --reload
# Yeh command hmari FastAPI app ko run karke requests sunne wala server start karti ha 




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Frontend aur backend alag jagah chal rahe hote hain
# Browser bolta hai:
# “Main direct baat nahi karne dunga”
# CORS bolta hai:
# "I allow it" ,  Agar CORS na ho → frontend kabhi backend se baat nahi karega





# ========== DATABASE (Simulated) ==========
fake_drugs_db = [
    {"id": 1, "name": "Metformin", "type": "Diabetes", "risk": 45},
    {"id": 2, "name": "Lamictal", "type": "Epilepsy", "risk": 85},
    {"id": 3, "name": "Aspirin", "type": "Pain Relief", "risk": 15},
]




# ========== API ENDPOINTS ==========
# Backend zinda hai ya nahi
# Available endpoints list , Frontend normally isko use nahi karta, ye developer ke liye hota hai.
@app.get("/")
async def root():
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
    
    
    



# The @ symbol is called a decorator in Python
# Decorators are special functions that modify the behavior of other functions or methods
# When we write @app.get("/health"), we are telling FastAPI:
# "Hey, this function below is a handler for HTTP GET requests on the /health path"


# 2. Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running",
        "status_code" : "200",
        "time": datetime.utcnow().isoformat()
    }
        
# The function returns a JSON response with some status info:
# "status": "healthy" — tells client the backend is okay.
# "message": "Backend is running"  a friendly message.
# "time": datetime.utcnow().isoformat() — current UTC time in ISO format
# When someone visits http://yourserver/health with a GET request, this function runs and sends back a JSON like:    
# { "status": "healthy", "message": "Backend is running", "time": "2025-12-26T14:00:00.000000" }

# async means Jab backend kisi slow kaam ka wait kar raha ho (jaise database, external API, file, network), to wo rukta nahi, balkay dusri
# requests handle karta rehta hai, Backend ek request par atak ke khara nahi rehta, wo ek waqt mein multiple users ko handle kar sakta hai
# main kam ha multiple users ki ek sth requests ko handle krna baghair ksi user ko wait krwye








@app.get("/api/search/{drug_name}")     # /api/search/Metformin
async def search_drug(drug_name: str):    # It means front-end mn jo likha jyga wo backend mn variable mn ml jyga
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
            similar_drugs.append({      # Backend data ko transform kar raha hai
                "target_drug": drug,
                "similarity_score": drug["risk"],   
                "risk_category": "high" if drug["risk"] > 50 else "medium" if drug["risk"] > 25 else "low"
            })
    
    print(f"Backend sending response: {len(similar_drugs)} results")
    
    # Yahin backend ka kaam khatam
    # JSON ban gaya
    #Frontend ko bhej diya

    return {
        "query_drug": drug_name,
        "similar_drugs": similar_drugs[:5],  # Limit to 5 for simplicity
        "total_found": len(similar_drugs),   
        "timestamp": datetime.utcnow().isoformat()
    }
    


# Frontend ko poora database dena
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