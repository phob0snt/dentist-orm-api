import os
import sys


sys.path.append('/app')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
from app.db.session import SessionLocal
from app.models.auth import AuthORM
from app.core.security import get_password_hash
from dotenv import load_dotenv

load_dotenv()

login = os.getenv("ADMIN_LOGIN", "admin")
password = os.getenv("ADMIN_PASSWORD", "admin123")

def create_admin():
    db = SessionLocal()

    try:
        existing_admin = db.query(AuthORM).filter(AuthORM.role == "admin").first()

        if existing_admin is not None:
            print(f"Админ уже существует: {existing_admin.login}")
            return existing_admin
        
        admin = AuthORM(
            login = login,
            password_hash = get_password_hash(password),
            role = "admin"
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"Админ успешно создан: {login}")

    except Exception as e:
        print(f"Ошибка при создании админа: {e}")
        db.rollback()
        raise

    finally:
        db.close()

if (__name__) == "__main__":
    create_admin()