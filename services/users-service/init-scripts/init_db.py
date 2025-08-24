import os
import sys


from app.db.session import create_tables

def init_database():
    """Инициализирует базу данных, создавая все таблицы"""
    create_tables()

if __name__ == "__main__":
    init_database()
