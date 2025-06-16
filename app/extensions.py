from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
migrate = Migrate()

server_error = {
    'status': 'error',
    'message': 'Terjadi kesalahan pada server.'
}

def log(message):
    try:
        with open('error.log', 'a') as file:
            file.write(f"{datetime.datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Gagal menulis ke log file: {e}")