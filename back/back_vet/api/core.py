from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins = [
    "http://localhost:8080",             
    "https://clinicfastpig.netlify.app",      # ваш домен на Netlify
]
import os
print(f"PORT env: {os.environ.get('PORT')}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)