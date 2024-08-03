import pandas as pd
import duckdb

# Функция для создания таблиц
def create_tables():
    conn = duckdb.connect('my.db')
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Final_cleaned (
        Entity VARCHAR,
        Code VARCHAR,
        Year BIGINT,
        Cellular_Subscription FLOAT,
        Internet_Users_Percent FLOAT,
        No_of_Internet_Users BIGINT,
        Broadband_Subscription FLOAT
    )
    """)
    conn.close()
    print("Таблица создана успешно")

# Функция для загрузки данных
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Загруженные данные из {file_path}:")
    print(data.head())  # Вывод первых строк данных для проверки

    # Вывод типов данных DataFrame
    print("Типы данных DataFrame до преобразования:")
    print(data.dtypes)

    # Приведение типов данных в DataFrame
    data['Year'] = data['Year'].astype('int64')
    data['Cellular Subscription'] = data['Cellular Subscription'].astype('float64')
    data['Internet Users(%)'] = data['Internet Users(%)'].astype('float64')
    data['No. of Internet Users'] = data['No. of Internet Users'].astype('int64')
    data['Broadband Subscription'] = data['Broadband Subscription'].astype('float64')

    # Убедимся, что названия столбцов совпадают с названиями в таблице
    data = data.rename(columns={
        "No. of Internet Users": "No_of_Internet_Users",
        "Cellular Subscription": "Cellular_Subscription",
        "Internet Users(%)": "Internet_Users_Percent",
        "Broadband Subscription": "Broadband_Subscription"
    })

    # Убедимся, что порядок столбцов совпадает с порядком в таблице
    data = data[['Entity', 'Code', 'Year', 'Cellular_Subscription', 'Internet_Users_Percent', 'No_of_Internet_Users', 'Broadband_Subscription']]

    # Проверка значений, чтобы убедиться, что они находятся в допустимом диапазоне
    data['No_of_Internet_Users'] = data['No_of_Internet_Users'].apply(lambda x: min(x, 2147483647))

    print("Типы данных после преобразования:")
    print(data.dtypes)

    conn = duckdb.connect('my.db')
    conn.register("temp_table", data)

    # Вставка данных построчно
    for _, row in data.iterrows():
        try:
            conn.execute("""
            INSERT INTO Final_cleaned (Entity, Code, Year, Cellular_Subscription, Internet_Users_Percent, No_of_Internet_Users, Broadband_Subscription)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row.tolist())
        except duckdb.ConversionException as e:
            print(f"Ошибка вставки строки: {row}")
            print(f"Ошибка: {e}")

    conn.close()
    print("Данные успешно загружены в таблицу Final_cleaned")

# Выполнение функций
create_tables()
load_data('source/Final_cleaned.csv')

