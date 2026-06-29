from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Allow origins for frontend url 
origins = [
    "http://localhost:5173"
]

app.add_middleware (
    CORSMiddleware,
    allow_origins = origins, #allow frontend url
    allow_credentials = True,
    allow_methods = ["*"], #Get, Put, Post, Delete, Update
    allow_headers = ["*"], #Allow headers
)

@app.get('/')
def home():
    return {
        "message": "CORS Enable API"        
    }