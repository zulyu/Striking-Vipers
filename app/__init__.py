"""Flask application factory and configuration."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_restx import Api

db = SQLAlchemy()


def create_app(config_name="development"):
    """Create and configure the Flask application.

    Args:
        config_name (str): The name of the configuration to use.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    # Initialize API with swagger docs
    api = Api(
        app,
        version="1.0",
        title="Striking Vipers API",
        description="API for Teachers, Classes, and Students",
        doc="/",  # This will serve the Swagger UI at the root URL
        prefix="/api"  # All API routes will be prefixed with /api
    )

    # Import and register API namespaces
    from app.api.routes import (
        TeacherList, TeacherResource,
        ClassList, ClassResource,
        StudentList, StudentResource,
        auth_ns
    )

    # Add auth namespace
    api.add_namespace(auth_ns, path='/api/auth')

    # Add resources to API
    api.add_resource(TeacherList, '/teachers')
    api.add_resource(TeacherResource, '/teachers/<int:teacher_id>')
    api.add_resource(ClassList, '/classes')
    api.add_resource(ClassResource, '/classes/<string:class_id>')
    api.add_resource(StudentList, '/students')
    api.add_resource(StudentResource, '/students/<int:student_id>')

    return app
