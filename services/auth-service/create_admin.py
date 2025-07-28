import getpass
from app.db.session import SessionLocal
from app.models.auth import AuthORM
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()

    try:
        existing_admin = db.query(AuthORM).filter(AuthORM.role == "admin").first()

        if existing_admin is not None:
            print(f"Админ уже существует: {existing_admin.login}")
            return existing_admin
        
        print("Создание администратора")
        print("-" * 40)

        login = input("Логин: ").strip()

        if not login:
            print("Логин не может быть пустым!")
            return None
        
        password = getpass.getpass("Пароль: ").strip()

        if not password:
            print("Пароль не может быть пустым!")
            return None
        
        password_confirm = getpass.getpass("Подтвердите пароль: ").strip()

        if password != password_confirm:
            print("Пароли должны совпадать")
            return None
        
        if (len(password) < 6):
            print("Пароль должен содержать не менее 6 символов")
            return None
        
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