import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEOCODING_API_KEY = os.getenv('GEOCODING_API_KEY')
    GRAPHHOPPER_API_KEY = os.getenv('GRAPHHOPPER_API_KEY')
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

    DEPOT_COORDS = os.getenv('DEPOT_COORDS')