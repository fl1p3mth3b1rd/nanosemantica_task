from os import environ

from sqlalchemy import create_engine

from src.settings import config


DB_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
DB_URL = DB_URL_TEMPLATE.format(**config["postgres"])

def create_dummy_db() -> None:
    """Создает таблицу с тестовыми данными"""
    engine = create_engine(DB_URL)
    conn = engine.connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            name VARCHAR(100),
            age INT,
            department VARCHAR(1000)
        );
        """
    )
    if bool(int(environ.get('create_dummy_data', 0))):
        conn.execute(
            """
            INSERT INTO users (name, age, department)
            VALUES
                ('Иван', 25, 'department_1'),
                ('Алексей', 26, 'department_2'),
                ('Ольга', 31, 'department_2'),
                ('Ксения', 40, 'department_3'),
                ('Андрей', 29, 'department_1');
            """
    )
    conn.close()
