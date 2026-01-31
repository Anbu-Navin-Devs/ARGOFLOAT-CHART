# Gunicorn configuration for Render deployment
# Handles long-running AI queries

# Timeout for worker processes (in seconds)
# AI queries can take 30-60 seconds
timeout = 120

# Number of worker processes
workers = 2

# Worker class
worker_class = "sync"

# Keep alive connections
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Graceful timeout
graceful_timeout = 30
