# Gunicorn configuration
bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
accesslog = "-"
errorlog = "-"
capture_output = True

# Security settings
forwarded_allow_ips = "*"
proxy_allow_ips = "*"

# Logging configuration
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout"
        }
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
} 