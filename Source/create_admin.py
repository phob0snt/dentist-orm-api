from app.core.security import get_password_hash
from app.models.manager import ManagerORM
from app.db.session import SessionLocal


def create_admin():

    db = SessionLocal()

    try:
        existing_admin = db.query(ManagerORM).filter(
            ManagerORM.is_admin == True).first()
        
        if existing_admin:
            print("Администратор уже существует")
            return
        
        admin_data = {
            "full_name": "Администратор",
            "login": "admin",
            "email": "admin123@mail.ru",
            "password": "admin123",
            "is_active": True,
            "is_admin": True
        }

        adminORM = ManagerORM(
            full_name=admin_data["full_name"],
            login=admin_data["login"],
            email=admin_data["email"],
            password_hash=get_password_hash(admin_data["password"]),
            is_active=admin_data["is_active"],
            is_admin=admin_data["is_admin"]
        )

        db.add(adminORM)
        db.commit()
        db.refresh(adminORM)

        print("Администратор успешно создан")
        print(f"Логин: {adminORM.login}")
        print(f"Пароль: {admin_data['password']}")

    except Exception as e:
        print(f"Произошла ошибка при создании администратора: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()