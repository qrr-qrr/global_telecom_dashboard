"""
Этот модуль обеспечивает подключение к базе данных DuckDB.
"""

import duckdb
import os

def get_connection(db_path='my.db'):
    """
    Устанавливает соединение с базой данных DuckDB.
    
    Args:
        db_path (str): Путь к файлу базы данных. По умолчанию 'my.db'.
    
    Returns:
        duckdb.DuckDBPyConnection: Объект соединения с базой данных.
    """
    if not os.path.exists(db_path):
        # Если файл не существует, создаем новую базу данных
        conn = duckdb.connect(db_path)
        conn.close()
    
    return duckdb.connect(db_path)