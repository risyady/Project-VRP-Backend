from flask import Flask
from config import Config
from flask_cors import CORS
from .extensions import *

from .routes import *
from .models import *

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, origins=['http://localhost:5173', 'https://your-production-domain.com'])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(kurir_bp, url_prefix='/api/v1/user')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(paket_bp, url_prefix='/api/v1/paket')
    app.register_blueprint(rute_bp, url_prefix='/api/v1/rute')
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')

    return app