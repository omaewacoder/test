# database.py
import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

def get_connection():
    """Создает и возвращает соединение с базой данных."""
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Успешное подключение к БД!")
        return connection
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def create_table(connection):
    """Создает тестовую таблицу, если она не существует."""
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()  # Фиксируем изменения!
        print("Таблица 'test_table' готова к работе.")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def insert_data(connection, message):
    """Вставляет новую запись в таблицу."""
    insert_query = "INSERT INTO test_table (message) VALUES (%s);"
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, (message,))
            connection.commit()
        print(f"Данные успешно добавлены: '{message}'")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")

def read_data(connection):
    """Читает и выводит все данные из таблицы."""
    select_query = "SELECT * FROM test_table;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("\nДанные в таблице:")
            for row in records:
                print(f"ID: {row[0]}, Message: '{row[1]}', Created: {row[2]}")
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")

# Главный блок для тестирования функций
if __name__ == "__main__":
    # Убедитесь, что ваш Docker-контейнер с Postgres запущен!
    conn = get_connection()

    if conn is not None:
        try:
            create_table(conn)
            insert_data(conn, "Первое тестовое сообщение из Python!")
            insert_data(conn, "Второе тестовое сообщение!")
            read_data(conn)
        finally:
            conn.close()  # Всегда закрываем соединение!
            print("\nСоединение с БД закрыто.")