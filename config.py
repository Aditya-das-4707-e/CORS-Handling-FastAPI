import os 
from dotenv import load_dotenv

load_dotenv() #Read .env file for environment variables

class Settings:
    #Allow origins for frontend url 
    origins = os.getenv("origins")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_URL = os.getenv("DB_URL")

settings = Settings()