"""Flask application factory and configuration."""

import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import config
from flask_restx import Api

db = SQLAlchemy()


def create_app(config_name="development"):
    """Create and configure the Flask application.

    Args:
        config_name (str): The name of the configuration to use.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Get the absolute path to the web_build directory
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    web_build_dir = os.path.join(base_dir, 'web_build')
    
    app = Flask(__name__, 
                static_folder=web_build_dir,
                static_url_path='')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Initialize API with swagger docs
    api = Api(
        app,
        version="1.0",
        title="Striking Vipers API",
        description="API for Teachers, Classes, and Students",
        doc="/api/",  # This will serve the Swagger UI at /api/
        prefix="/api",  # All API routes will be prefixed with /api
        catch_all_404s=True,  # Enable catching 404 errors
        serve_challenge_on_401=True,  # Enable serving challenge on 401
        validate=True  # Enable request validation
    )

    # Import and register API namespaces
    from app.api.routes import (
        TeacherList, TeacherResource,
        ClassList, ClassResource,
        StudentList, StudentResource,
        auth_ns
    )

    # Add auth namespace
    api.add_namespace(auth_ns, path='/auth')

    # Add resources to API
    api.add_resource(TeacherList, '/teachers')
    api.add_resource(TeacherResource, '/teachers/<int:teacher_id>')
    api.add_resource(ClassList, '/classes')
    api.add_resource(ClassResource, '/classes/<string:class_id>')
    api.add_resource(StudentList, '/students')
    api.add_resource(StudentResource, '/students/<int:student_id>')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return {'message': 'Resource not found'}, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """405 error handler"""
        return {'message': 'Method not allowed'}, 405

    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return {'message': 'Internal server error'}, 500

    return app
