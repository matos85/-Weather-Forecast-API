from database import SessionLocal
from db_models import User
from utils import hash_password

db = SessionLocal()

admin = User(
    login="admin1",
    password=hash_password("adminpassword"),
    email="adm1in@example.com",
    city="Admin1City",
    is_admin=True
)

try:
    db.add(admin)
    db.commit()
    print("Администратор успешно создан")
except:
    db.rollback()
    print("Ошибка: администратор с таким логином, email или Telegram уже существует")
finally:
    db.close()