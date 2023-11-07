# __init__

import os

from flask import Flask, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from api.config import Config

db = SQLAlchemy()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config.get_config())

    app.config['SESSION_COOKIE_MAX_SIZE'] = 300
    db.init_app(app)
    bcrypt.init_app(app)

    # blueprints
    from api.v1.routes.authorizations import auth_bp
    from api.v1.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app

