"""
Этот модуль отвечает за извлечение данных из базы данных и создание DataFrame для визуализации.
"""

import pandas as pd
from connector import get_connection

def get_digital_divide_data():
    """
    Извлекает данные о цифровом разрыве.
    """
    conn = get_connection()
    df = conn.execute("SELECT * FROM digital_divide").df()
    conn.close()
    return df

def get_internet_growth_data():
    """
    Извлекает данные о темпах роста интернет-проникновения.
    """
    conn = get_connection()
    df = conn.execute("SELECT * FROM internet_growth").df()
    conn.close()
    return df

def get_mobile_vs_broadband_data():
    """
    Извлекает данные для сравнения развития мобильной связи и широкополосного интернета.
    """
    conn = get_connection()
    df = conn.execute("SELECT * FROM mobile_vs_broadband").df()
    conn.close()
    return df

def get_telecom_trends_data():
    """
    Извлекает общие данные о телекоммуникационных трендах для прогнозирования.
    """
    conn = get_connection()
    df = conn.execute("SELECT * FROM Final_cleaned").df()
    conn.close()
    return df