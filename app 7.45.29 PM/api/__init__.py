"""API package initialization."""

from flask import Flask, jsonify, send_from_directory
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.config import config
import os

db = SQLAlchemy()

# This file can be empty as the routes are defined in routes.py
# and imported where needed

def create_app(config_name="default"):
    # Get the absolute path to the web_build directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    web_build_dir = os.path.join(base_dir, 'web_build')
    
    app = Flask(__name__, 
                static_folder=web_build_dir,
                static_url_path='')
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Create API instance with default configuration
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

    # Register namespaces with explicit names
    from .routes import auth_ns, teacher_ns, class_ns, student_ns
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(teacher_ns, path='/teachers')
    api.add_namespace(class_ns, path='/classes')
    api.add_namespace(student_ns, path='/students')

    # Error handlers using Flask-RESTX
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """405 error handler"""
        return jsonify({'message': 'Method not allowed'}), 405

    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return jsonify({'message': 'Internal server error'}), 500

    # Add a route for the API root that serves the Swagger UI
    @app.route('/api/')
    def api_root():
        """API root endpoint"""
        return api.render_root()

    # Add a route for the Swagger JSON
    @app.route('/api/swagger.json')
    def swagger_json():
        """Swagger JSON endpoint"""
        return api.as_postman()

    return app
