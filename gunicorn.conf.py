import multiprocessing

workers = 1  # Для начала используем только одного работника
threads = 2
timeout = 120
bind = "0.0.0.0:$PORT"