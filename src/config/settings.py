# config/settings.py:
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CREDENTIALS_AWS = os.getenv("CREDENTIALS_AWS")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
    DEBUG = True
    # DEBUG = os.getenv("FLASK_ENV") == "development"

