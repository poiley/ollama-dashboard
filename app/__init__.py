from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import pytz
import os

class Config:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
    OLLAMA_PORT = int(os.getenv('OLLAMA_PORT', 11434))
    MAX_HISTORY = int(os.getenv('MAX_HISTORY', 50))
    HISTORY_FILE = os.getenv('HISTORY_FILE', 'history.json')
    STATIC_URL_PATH = ''
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

def create_app():
    app = Flask(__name__,
                static_url_path=Config.STATIC_URL_PATH,
                static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": "*",
            "expose_headers": "*"
        }
    })
    
    # Register template filters
    @app.template_filter('datetime')
    def format_datetime(value):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00').split('.')[0])
            except ValueError:
                return value
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @app.template_filter('time_ago')
    def time_ago(value):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00').split('.')[0])
            except ValueError:
                return value
        
        now = datetime.now(pytz.UTC)
        if isinstance(value, datetime):
            value = value.replace(tzinfo=pytz.UTC)
        
        diff = now - value
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''}"
    
    # Register blueprints
    from app.routes import bp as main_bp
    from app.routes.main import init_app as init_main_bp
    app.register_blueprint(main_bp)
    init_main_bp(app)  # Initialize the blueprint with the app
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    # Health check endpoint
    @app.route('/ping')
    def ping():
        return jsonify({"status": "ok"})
    
    return app 