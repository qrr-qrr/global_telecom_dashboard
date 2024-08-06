import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
bind = "0.0.0.0:$PORT"