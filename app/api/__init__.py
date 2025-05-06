"""API package initialization."""

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="Striking Vipers API",
        description="API for Teachers, Classes, and Students",
        doc="/swagger",
    )

    from .routes import api as teacher_api

    api.add_namespace(teacher_api)

    return app


# This file can be empty as the routes are defined in routes.py
# and imported where needed
