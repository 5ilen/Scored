from datetime import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'teacher' или 'student'
    students = db.relationship('Student', backref='teacher', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    education_form = db.Column(db.String(20), nullable=False)  # 'day', 'evening', 'distance'
    group_name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grades = db.relationship('Grade', backref='student', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    assessment_type = db.Column(db.String(20), nullable=False)  # 'exam' или 'credit'

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    grade = db.Column(db.String(5), nullable=False)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
