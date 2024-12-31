# Gunicorn configuration
bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = "info"

# Security settings
forwarded_allow_ips = "*"
proxy_allow_ips = "*" 