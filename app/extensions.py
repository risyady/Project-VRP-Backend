from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app
import datetime
import requests

db = SQLAlchemy()
migrate = Migrate()

server_error = {
    'status': 'error',
    'message': 'Terjadi kesalahan pada server.'
}

def get_coords(address):
    api_key = current_app.config.get('GRAPHHOPPER_API_KEY')
    if not api_key:
        log("Error: GRAPHHOPPER_API_KEY tidak ditemukan di konfigurasi.")
        return None, None
    
    base_url = "https://graphhopper.com/api/1/geocode"
    params = {
        'q': address,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Periksa apakah 'hits' ada di dalam data dan tidak kosong
        if data and data.get('hits'):
            location = data['hits'][0]['point']
            log(f"GraphHopper menemukan koordinat: {location.get('lat')}, {location.get('lng')}")
            return location.get('lat'), location.get('lng')
        else:
            # Ini akan menangani kasus jika alamat tidak ditemukan
            log(f"GraphHopper tidak dapat menemukan koordinat untuk alamat: {address}")
            return None, None
    except requests.exceptions.RequestException as e:
        log(f"Error saat menghubungi GraphHopper API: {e}")
        return None, None

def log(message):
    try:
        with open('error.log', 'a') as file:
            file.write(f"{datetime.datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Gagal menulis ke log file: {e}")