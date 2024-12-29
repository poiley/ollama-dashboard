from flask import Flask, jsonify, render_template, url_for
import requests
from datetime import datetime
import pytz
from datetime import datetime, timezone
import time

app = Flask(__name__, static_url_path='/static', static_folder='static')

OLLAMA_PORT = 11434
API_URL = f"http://localhost:{OLLAMA_PORT}/api/ps"

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

@app.route('/')
def home():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        models = data.get('models', [])
        
        # Format expiration times
        for model in models:
            if model.get('expires_at'):
                expires_dt = datetime.fromisoformat(model['expires_at'].replace('Z', '+00:00'))
                local_dt = expires_dt.astimezone()  # Convert to local time
                relative_time = format_relative_time(expires_dt)
                tz_abbr = get_timezone_abbr()
                model['expires_at'] = {
                    'local': local_dt.strftime(f'%-I:%M %p, %b %-d ({tz_abbr})'),  # e.g. "2:44 PM, Dec 29 (PST)"
                    'relative': relative_time
                }
                
    except Exception as e:
        models = []
        error_message = str(e)
        return render_template('index.html', models=models, error=error_message)

    return render_template('index.html', models=models, error=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
