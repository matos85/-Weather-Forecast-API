import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1  # Количество воркеров
bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"