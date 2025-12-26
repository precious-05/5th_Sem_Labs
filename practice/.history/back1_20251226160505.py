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
# Yeh command hmari FastAPI app ko run karke requests sunne wala server start karta hai.