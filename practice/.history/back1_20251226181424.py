from fastapi import FastAPI
# Ye line kehti hai: fastapi package se FastAPI class ko import kar lo apne program mein
from datetime import datetime

app = FastAPI()
# app FastAPI class ka ek instance (object) hai, jiske through hum apni web application ko define aur chalate hain
# FastAPI server ka ek instance (app) banya ha yhan jo backend web server ki tarah kaam karta hai
# Lekin ye sirf server ka "app object" banata hai, jo:
# Requests receive karne ke liye ready hota hai,
# Aur hmary defined routes (URLs) ko handle karta hai
# Lekin real server chalane ke liye hme is app ko run karna hota hai, jaise:
# uvicorn main:app --reload
# Yeh command hmari FastAPI app ko run karke requests sunne wala server start karti ha 




# The @ symbol is called a decorator in Python
# Decorators are special functions that modify the behavior of other functions or methods
# When we write @app.get("/health"), we are telling FastAPI:
# "Hey, this function below is a handler for HTTP GET requests on the /health path"


@app.get("/health")
async def health_check():
        return {
            "status": "healthy",
            "message": "Backend is running",
            "time" : datetime.utcnow.isoformat()
        }