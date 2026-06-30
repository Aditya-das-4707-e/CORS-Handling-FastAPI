from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

app.add_middleware (
    CORSMiddleware,
    allow_origins = settings.origins, #allow frontend url
    allow_credentials = True,
    allow_methods = ["*"], #Get, Put, Post, Delete, Update
    allow_headers = ["*"], #Allow headers
)

@app.get('/')
def home():
    return {
        "message": "CORS Enable API"        
    }