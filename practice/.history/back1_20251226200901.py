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

