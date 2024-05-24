from app import create_app, db

def reset_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("База данных успешно сброшена.")

if __name__ == "__main__":
    reset_database()
