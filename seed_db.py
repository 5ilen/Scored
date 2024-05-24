from app import create_app, db
from app.models.models import User, Student, Subject, Grade
from datetime import datetime

def seed_database():
    app = create_app()
    with app.app_context():
        # Создание пользователей
        teachers = [
            User(username=f'преподаватель{i}', email=f'teacher{i}@example.com', password=f'teacher{i}', role='teacher')
            for i in range(1, 6)
        ]
        students = [
            User(username=f'студент{i}', email=f'student{i}@example.com', password=f'student{i}', role='student')
            for i in range(1, 21)
        ]
        
        for teacher in teachers:
            db.session.add(teacher)
        
        for student in students:
            db.session.add(student)
        
        db.session.commit()
        
        print("Пользователи добавлены")

        # Создание студентов
        students_db = User.query.filter_by(role='student').all()
        for i, user in enumerate(students_db, 1):
            student = Student(
                name=f'Студент {i}', 
                admission_year=2022, 
                education_form='дневная', 
                group_name=f'Группа {i % 5 + 1}', 
                user_id=user.id
            )
            db.session.add(student)
        
        db.session.commit()
        print("Студенты добавлены")

        # Создание предметов
        subjects = [
            Subject(name='Математика', semester=1, hours=100, assessment_type='экзамен'),
            Subject(name='Физика', semester=1, hours=80, assessment_type='зачет'),
            Subject(name='Программирование', semester=1, hours=120, assessment_type='экзамен'),
            Subject(name='История', semester=2, hours=60, assessment_type='зачет'),
            Subject(name='Химия', semester=2, hours=90, assessment_type='экзамен')
        ]
        
        for subject in subjects:
            db.session.add(subject)
        
        db.session.commit()
        print("Предметы добавлены")
        
        # Создание оценок
        students_db = Student.query.all()
        subjects_db = Subject.query.all()
        for student in students_db:
            for subject in subjects_db:
                grade = Grade(
                    year=2023, 
                    semester=subject.semester, 
                    student_id=student.id, 
                    subject_id=subject.id, 
                    grade='A' if student.id % 2 == 0 else 'B'
                )
                db.session.add(grade)
        
        db.session.commit()
        print("Оценки добавлены")

        # Проверка содержимого базы данных
        users = User.query.all()
        print(f"Всего пользователей: {len(users)}")
        for user in users:
            print(user.username, user.email)

if __name__ == "__main__":
    seed_database()
