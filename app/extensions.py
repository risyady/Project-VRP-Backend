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
    # GraphHopper GeoCoding
    """ api_key = current_app.config.get('GRAPHHOPPER_API_KEY')
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

        if data and data.get('hits'):
            location = data['hits'][0]['point']
            log(f"GraphHopper menemukan koordinat: {location.get('lat')}, {location.get('lng')}")
            return location.get('lat'), location.get('lng')
        else:
            log(f"GraphHopper tidak dapat menemukan koordinat untuk alamat: {address}")
            return None, None
    except requests.exceptions.RequestException as e:
        log(f"Error saat menghubungi GraphHopper API: {e}")
        return None, None """
    
    api_key = current_app.config.get('SERPAPI_API_KEY')
    if not api_key:
        log("Error: SERPAPI_API_KEY tidak ditemukan di konfigurasi.")
        return None, None
    
    base_url = "https://serpapi.com/search.json"
    params = {
        'engine': 'google_maps',
        'q': address,
        'hl': 'id',
        'gl': 'id',
        'api_key': api_key,
        'async': 'true'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            location = data['place_results']['gps_coordinates']
            return location.get('latitude'), location.get('longitude')
    
        else: 
            log(f"SerpAPI tidak dapat menemukan koordinat untuk alamat: {address}")
            return None, None
        
    except requests.exceptions.RequestException as e:
        log(f"Error saat menghubungi SerpAPI: {e}")
        return None, None

def format_vrp_solver(kurirs, pakets, depot_coords):
    vehicles = []
    for kurir in kurirs:
        vehicle = {
            "vehicle_id": str(kurir.id),
            "start_address": {
                "location_id": "gudang",
                "lat": depot_coords[0],
                "lon": depot_coords[1]
            },
            "type_id": "scooter"
        }
        vehicles.append(vehicle)

    services = []
    for paket in pakets:
        #koordinat = paket.get('latitude'), paket.get('longitude')
        service = {
            "id": str(paket.id),
            "name": paket.resi,
            "type": "service",
            "address": {
                "location_id": f"loc_{paket.id}",
                "lat": paket.latitude,
                "lon": paket.longitude,
            },
            "size": [paket.berat]
        }
        services.append(service)

    vehicle_types = [
        {
            "type_id": "scooter",
            "profile": "scooter",
            "capacity": [50000]
        }
    ]

    request_body = {
        "configuration": {
            "routing": {
                "calc_points": True,
                "return_snapped_waypoints": True
            }
        },
        "objectives": [
            {
                "type": "min-max",
                "value": "completion_time"
            },
            {
                "type": "min-max",
                "value": "activities"
            }
        ],
        "vehicles": vehicles,
        "vehicle_types": vehicle_types,
        "services": services
    }

    return request_body

def vrp_solver(kurirs, pakets, depot_coords):
    api_key = current_app.config.get('GRAPHHOPPER_API_KEY')
    if not api_key:
        log("Error: GRAPHHOPPER_API_KEY tidak ditemukan di konfigurasi.")
        return None
    
    GRAPHOPPER_VRP_ENDPOINT = f"https://graphhopper.com/api/1/vrp?key={api_key}"
    try:
        payload = format_vrp_solver(kurirs, pakets, depot_coords)
        
        if not payload.get("services"):
            return {"error": "Tidak ada data paket yang valid untuk diproses."}, 400
        
        #return payload, 200

        headers = {"Content-Type": "application/json"}
        response = requests.post(GRAPHOPPER_VRP_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status() 

        return response.json(), response.status_code

    except ValueError as ve:
        return {"error": str(ve)}, 400
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error terjadi: {http_err}", "details": response.text}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error terjadi: {req_err}"}, 500
    except Exception as e:
        return {"error": f"Terjadi kesalahan internal: {e}"}, 500

def log(message):
    try:
        with open('error.log', 'a') as file:
            file.write(f"{datetime.datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Gagal menulis ke log file: {e}")