import random
from faker import Faker
from app import create_app, db, bcrypt
from app.models.models import User, Student, Subject, Grade

fake = Faker('ru_RU')

def generate_students(num_students):
    students = []
    education_forms = ['дневная', 'вечерняя', 'заочная']
    group_names = ['Группа 1', 'Группа 2', 'Группа 3', 'Группа 4', 'Группа 5']

    for _ in range(num_students):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=bcrypt.generate_password_hash(fake.password()).decode('utf-8'),
            role='student'
        )
        db.session.add(user)
        db.session.commit()

        student = Student(
            name=f"{fake.last_name()} {fake.first_name()} {fake.middle_name()}",
            admission_year=random.randint(2018, 2023),
            education_form=random.choice(education_forms),
            group_name=random.choice(group_names),
            user_id=user.id
        )
        students.append(student)
        db.session.add(student)

    db.session.commit()
    return students

def generate_subjects():
    subjects_data = [
        {'name': 'Математика', 'semester': 1, 'hours': 100, 'assessment_type': 'экзамен'},
        {'name': 'Физика', 'semester': 1, 'hours': 80, 'assessment_type': 'зачет'},
        {'name': 'Программирование', 'semester': 1, 'hours': 120, 'assessment_type': 'экзамен'},
        {'name': 'История', 'semester': 2, 'hours': 60, 'assessment_type': 'зачет'},
        {'name': 'Химия', 'semester': 2, 'hours': 90, 'assessment_type': 'экзамен'},
        {'name': 'Биология', 'semester': 2, 'hours': 70, 'assessment_type': 'зачет'},
        {'name': 'Литература', 'semester': 1, 'hours': 50, 'assessment_type': 'зачет'},
        {'name': 'Физическая культура', 'semester': 1, 'hours': 30, 'assessment_type': 'зачет'}
    ]

    subjects = []

    for subj in subjects_data:
        subject = Subject(
            name=subj['name'],
            semester=subj['semester'],
            hours=subj['hours'],
            assessment_type=subj['assessment_type']
        )
        subjects.append(subject)
        db.session.add(subject)

    db.session.commit()
    return subjects

def generate_grades(students, subjects):
    grades = ['5', '4', '3', '2']

    for student in students:
        for subject in subjects:
            grade = Grade(
                year=random.randint(2019, 2023),
                semester=subject.semester,
                student_id=student.id,
                subject_id=subject.id,
                grade=random.choice(grades)
            )
            db.session.add(grade)

    db.session.commit()

def seed_database():
    app = create_app()
    with app.app_context():
        # Удаление всех данных из таблиц
        db.drop_all()
        db.create_all()

        # Создание преподавателей
        teachers = [
            User(username=f'teacher{i}', email=f'teacher{i}@example.com', password=bcrypt.generate_password_hash(f'teacher{i}').decode('utf-8'), role='teacher')
            for i in range(1, 6)
        ]
        
        for teacher in teachers:
            db.session.add(teacher)
        
        db.session.commit()
        
        print("Преподаватели добавлены")

        # Создание студентов
        students = generate_students(50)
        print("Студенты добавлены")

        # Создание предметов
        subjects = generate_subjects()
        print("Предметы добавлены")
        
        # Создание оценок
        generate_grades(students, subjects)
        print("Оценки добавлены")

        # Проверка содержимого базы данных
        users = User.query.all()
        print(f"Всего пользователей: {len(users)}")
        for user in users:
            print(user.username, user.email)

if __name__ == "__main__":
    seed_database()
