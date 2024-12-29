from flask import Flask, jsonify, render_template, url_for
import requests
from datetime import datetime
import pytz
from datetime import datetime, timezone
import time
import json
from collections import deque
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

OLLAMA_PORT = 11434
API_URL = f"http://localhost:{OLLAMA_PORT}/api/ps"
HISTORY_FILE = 'history.json'
MAX_HISTORY = 50

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                return deque(history, maxlen=MAX_HISTORY)
        return deque(maxlen=MAX_HISTORY)
    except:
        return deque(maxlen=MAX_HISTORY)

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(list(history), f)

history = load_history()

def get_timezone_abbr():
    return time.strftime('%Z')

def format_relative_time(target_dt):
    now = datetime.now(timezone.utc)
    diff = target_dt - now
    
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    if days > 0:
        if hours > 12:  # Round up to next day
            days += 1
        return f"about {days} {'day' if days == 1 else 'days'}"
    elif hours > 0:
        if minutes > 30:  # Round up to next hour
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

def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

@app.route('/')
def home():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        models = data.get('models', [])
        
        # Format model data and create history entry
        current_models = []
        for model in models:
            # Format size
            model['formatted_size'] = format_size(model['size'])
            
            # Format families
            families = model.get('details', {}).get('families', [])
            if families:
                model['families_str'] = ', '.join(families)
            else:
                model['families_str'] = model.get('details', {}).get('family', 'Unknown')
            
            # Format expiration times
            if model.get('expires_at'):
                expires_dt = datetime.fromisoformat(model['expires_at'].replace('Z', '+00:00'))
                local_dt = expires_dt.astimezone()
                relative_time = format_relative_time(expires_dt)
                tz_abbr = get_timezone_abbr()
                model['expires_at'] = {
                    'local': local_dt.strftime(f'%-I:%M %p, %b %-d ({tz_abbr})'),
                    'relative': relative_time
                }
            
            current_models.append({
                'name': model['name'],
                'families': model.get('families_str', ''),
                'parameter_size': model.get('details', {}).get('parameter_size', ''),
                'size': model.get('formatted_size', '')
            })
        
        # Add to history if models list changed
        if current_models:
            timestamp = datetime.now().isoformat()
            history.appendleft({
                'timestamp': timestamp,
                'models': current_models
            })
            save_history(history)
                
    except Exception as e:
        models = []
        error_message = str(e)
        return render_template('index.html', models=models, error=error_message)

    return render_template('index.html', models=models, error=None, history=list(history))

@app.template_filter('datetime')
def format_datetime(value):
    dt = datetime.fromisoformat(value)
    local_dt = dt.astimezone()  # Convert to local timezone
    tz_abbr = get_timezone_abbr()
    return local_dt.strftime(f'%-I:%M %p, %b %-d ({tz_abbr})')

@app.template_filter('time_ago')
def time_ago(value):
    """Convert timestamp to 'time ago' format"""
    dt = datetime.fromisoformat(value)
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

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
