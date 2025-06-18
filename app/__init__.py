from flask import Flask
from config import Config
from flask_cors import CORS
from .extensions import *

from .routes import *
from .models import *

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        origins="http://localhost:5173",
        supports_credentials=True
    )

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(kurir_bp, url_prefix='/user')

    return app