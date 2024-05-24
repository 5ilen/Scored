from app import db

def reset_database():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    reset_database()
    print("База данных успешно сброшена.")
