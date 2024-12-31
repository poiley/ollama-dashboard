from flask import current_app
import requests
from datetime import datetime, timezone
import time
import json
import os
from collections import deque

class OllamaService:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        else:
            self.history = deque(maxlen=50)  # Default max history

    def init_app(self, app):
        """Initialize the service with the Flask app"""
        self.app = app
        with self.app.app_context():
            self.history = self.load_history()

    def get_api_url(self):
        try:
            host = self.app.config.get('OLLAMA_HOST')
            port = self.app.config.get('OLLAMA_PORT')
            if not host or not port:
                raise ValueError(f"Missing configuration: OLLAMA_HOST={host}, OLLAMA_PORT={port}")
            return f"http://{host}:{port}/api/ps"
        except Exception as e:
            raise Exception(f"Failed to connect to Ollama server: {str(e)}. Please ensure Ollama is running and accessible.")

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def format_relative_time(self, target_dt):
        now = datetime.now(timezone.utc)
        diff = target_dt - now
        
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        
        if days > 0:
            if hours > 12:
                days += 1
            return f"about {days} {'day' if days == 1 else 'days'}"
        elif hours > 0:
            if minutes > 30:
                hours += 1
            return f"about {hours} {'hour' if hours == 1 else 'hours'}"
        elif minutes > 0:
            if minutes < 5:
                return "a few minutes"
            elif minutes < 15:
                return "about 10 minutes"
            elif minutes < 25:
                return "about 20 minutes"
            elif minutes < 45:
                return "about 30 minutes"
            else:
                return "about an hour"
        else:
            return "less than a minute"

    def get_running_models(self):
        try:
            response = requests.get(self.get_api_url(), timeout=5)
            response.raise_for_status()
            data = response.json()
            models = data.get('models', [])
            
            current_models = []
            for model in models:
                # Format size
                model['formatted_size'] = self.format_size(model['size'])
                
                # Format families
                families = model.get('details', {}).get('families', [])
                if families:
                    model['families_str'] = ', '.join(families)
                else:
                    model['families_str'] = model.get('details', {}).get('family', 'Unknown')
                
                # Format expiration times
                if model.get('expires_at'):
                    if model['expires_at'] == 'Stopping':
                        model['expires_at'] = {
                            'local': 'Stopping...',
                            'relative': 'Process is stopping'
                        }
                    else:
                        try:
                            # Handle microseconds by truncating them
                            expires_at = model['expires_at'].replace('Z', '+00:00')
                            expires_at = expires_at.split('.')[0] + '+00:00'
                            expires_dt = datetime.fromisoformat(expires_at)
                            local_dt = expires_dt.astimezone()
                            relative_time = self.format_relative_time(expires_dt)
                            tz_abbr = time.strftime('%Z')
                            model['expires_at'] = {
                                'local': local_dt.strftime(f'%-I:%M %p, %b %-d ({tz_abbr})'),
                                'relative': relative_time
                            }
                        except Exception as e:
                            model['expires_at'] = {
                                'local': 'Invalid date',
                                'relative': 'Unknown'
                            }
                
                current_models.append({
                    'name': model['name'],
                    'families': model.get('families_str', ''),
                    'parameter_size': model.get('details', {}).get('parameter_size', ''),
                    'size': model.get('formatted_size', '')
                })
            
            if current_models:
                self.update_history(current_models)
            
            return models
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to Ollama server. Please ensure it's running and accessible.")
        except requests.exceptions.Timeout:
            raise Exception("Connection to Ollama server timed out. Please check your network connection.")
        except Exception as e:
            raise Exception(f"Error fetching models: {str(e)}")

    def load_history(self):
        try:
            history_file = self.app.config['HISTORY_FILE']
            max_history = self.app.config['MAX_HISTORY']
            
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
                    return deque(history, maxlen=max_history)
            else:
                with open(history_file, 'w') as f:
                    json.dump([], f)
                return deque(maxlen=max_history)
        except Exception as e:
            print(f"Error handling history file: {str(e)}")
            return deque(maxlen=50)  # Default max history

    def update_history(self, models):
        timestamp = datetime.now().isoformat()
        self.history.appendleft({
            'timestamp': timestamp,
            'models': models
        })
        self.save_history()

    def save_history(self):
        with open(self.app.config['HISTORY_FILE'], 'w') as f:
            json.dump(list(self.history), f)

    def format_datetime(self, value):
        try:
            if isinstance(value, str):
                # Handle timezone offset in the ISO format string
                dt = datetime.fromisoformat(value.replace('Z', '+00:00').split('.')[0])
            else:
                dt = value
            local_dt = dt.astimezone()
            tz_abbr = time.strftime('%Z')
            return local_dt.strftime(f'%-I:%M %p, %b %-d ({tz_abbr})')
        except Exception as e:
            return str(value)

    def format_time_ago(self, value):
        try:
            if isinstance(value, str):
                # Handle timezone offset in the ISO format string
                dt = datetime.fromisoformat(value.replace('Z', '+00:00').split('.')[0])
            else:
                dt = value
            
            now = datetime.now(dt.tzinfo)
            diff = now - dt
            
            minutes = diff.total_seconds() / 60
            hours = minutes / 60
            
            if hours >= 1:
                return f"{int(hours)} {'hour' if int(hours) == 1 else 'hours'}"
            elif minutes >= 1:
                return f"{int(minutes)} {'minute' if int(minutes) == 1 else 'minutes'}"
            else:
                return "less than a minute"
        except Exception as e:
            return str(value) 