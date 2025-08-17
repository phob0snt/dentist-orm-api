import os
import sys


sys.path.append('/app')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import create_tables

def init_database():
    """Инициализирует базу данных, создавая все таблицы"""
    create_tables()

if __name__ == "__main__":
    init_database()
