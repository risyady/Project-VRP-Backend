from flask import Flask
from config import Config
from flask_cors import CORS
from .extensions import *

from .models import *

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    return app