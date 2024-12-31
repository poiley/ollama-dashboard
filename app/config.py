import os

class Config:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
    OLLAMA_PORT = int(os.getenv('OLLAMA_PORT', 11434))
    MAX_HISTORY = int(os.getenv('MAX_HISTORY', 50))
    HISTORY_FILE = os.getenv('HISTORY_FILE', 'history.json')
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    CORS_RESOURCES = {r"/*": {"origins": "*"}}
    
    # Flask settings
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates' 