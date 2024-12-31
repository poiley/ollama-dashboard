from flask import render_template, current_app
from app.services.ollama import OllamaService
from app.routes import bp
from datetime import datetime

# Initialize service without app
ollama_service = OllamaService()

@bp.route('/')
def index():
    try:
        # Get the current app context
        if not ollama_service.app:
            ollama_service.init_app(current_app)
        models = ollama_service.get_running_models()
        return render_template('index.html', 
                             models=models, 
                             error=None,
                             timezone=datetime.now().strftime('%Z'))
    except Exception as e:
        return render_template('index.html', 
                             models=[], 
                             error=str(e),
                             timezone=datetime.now().strftime('%Z'))

@bp.route('/api/test')
def test():
    return {"message": "API is working"}

def init_app(app):
    """Initialize the blueprint with the app"""
    ollama_service.init_app(app)
    app.template_filter('datetime')(format_datetime)
    app.template_filter('time_ago')(time_ago)

def format_datetime(value):
    return ollama_service.format_datetime(value)

def time_ago(value):
    return ollama_service.format_time_ago(value) 