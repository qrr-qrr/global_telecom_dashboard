import duckdb

# Подключение к базе данных
conn = duckdb.connect('my.db')

# Выполнение SQL-запроса для проверки данных
result = conn.execute("SELECT * FROM Final_cleaned LIMIT 5").fetchdf()

# Вывод результатов
print(result)

# Закрытие соединения
conn.close()
