from fastapi import FastAPI
# Ye line kehti hai: fastapi package se FastAPI class ko import kar lo apne program mein
from datetime import datetime

app = FastAPI()
# app FastAPI class ka ek instance (object) hai, jiske through hum apni web application ko define aur chalate hain
# FastAPI server ka ek instance (app) banya ha yhan jo backend web server ki tarah kaam karta hai
# 