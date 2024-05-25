import unittest
from app import create_app, db, bcrypt
from app.models.models import User, Student, Subject, Grade

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Создаем тестовых пользователей с зашифрованными паролями
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            teacher = User(username='testteacher', email='testteacher@example.com', password=hashed_password, role='teacher')
            student_user = User(username='teststudent', email='teststudent@example.com', password=hashed_password, role='student')
            db.session.add(teacher)
            db.session.add(student_user)
            db.session.commit()

            student = Student(name='Студент 1', admission_year=2022, education_form='дневная', group_name='Группа 1', user_id=student_user.id)
            db.session.add(student)

            subject = Subject(name='Математика', semester=1, hours=100, assessment_type='экзамен')
            db.session.add(subject)

            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добро пожаловать'.encode('utf-8'), response.data)

    def test_register(self):
        response = self.client.post('/register', data=dict(
            username='testuser2',
            email='testuser2@example.com',
            password='password',
            confirm_password='password',
            role='student'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваш аккаунт был создан! Вы можете войти в систему'.encode('utf-8'), response.data)

    def test_login(self):
        response = self.client.post('/login', data=dict(
            email='testteacher@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Личный кабинет преподавателя'.encode('utf-8'), response.data)

    def test_logout(self):
        self.client.post('/login', data=dict(
            email='testteacher@example.com',
            password='password'
        ), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добро пожаловать'.encode('utf-8'), response.data)

    def test_add_student(self):
        self.client.post('/login', data=dict(
            email='testteacher@example.com',
            password='password'
        ), follow_redirects=True)
        response = self.client.post('/student/add', data=dict(
            name='Студент 2',
            admission_year=2022,
            education_form='дневная',
            group_name='Группа 2'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Студент добавлен!'.encode('utf-8'), response.data)

    def test_add_subject(self):
        self.client.post('/login', data=dict(
            email='testteacher@example.com',
            password='password'
        ), follow_redirects=True)
        response = self.client.post('/subject/add', data=dict(
            name='Физика',
            semester=1,
            hours=100,
            assessment_type='экзамен'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Дисциплина добавлена!'.encode('utf-8'), response.data)

    def test_add_grade(self):
        self.client.post('/login', data=dict(
            email='testteacher@example.com',
            password='password'
        ), follow_redirects=True)
        with self.app.app_context():
            student = Student.query.first()
            subject = Subject.query.first()

        response = self.client.post('/grade/add', data=dict(
            year=2023,
            semester=1,
            student_id=student.id,
            subject_id=subject.id,
            grade='5'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Оценка добавлена!'.encode('utf-8'), response.data)

if __name__ == "__main__":
    unittest.main()
