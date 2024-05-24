from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.forms.forms import RegistrationForm, LoginForm, StudentForm, SubjectForm, GradeForm
from app.models.models import User, Student, Subject, Grade
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('main.dashboard_teacher'))
        elif current_user.role == 'student':
            return redirect(url_for('main.dashboard_student'))
    return render_template('home.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('main.dashboard_teacher'))
        elif current_user.role == 'student':
            return redirect(url_for('main.dashboard_student'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            form.email.errors.append('Этот адрес электронной почты уже используется. Пожалуйста, выберите другой.')
        elif form.role.data == 'teacher' and form.access_code.data != '1':
            form.access_code.errors.append('Неверный код доступа для преподавателей.')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
            db.session.add(user)
            db.session.commit()

            if form.role.data == 'student':
                student = Student(name=form.username.data, admission_year=datetime.now().year, 
                                  education_form='day', group_name='default', user_id=user.id)
                db.session.add(student)
                db.session.commit()

            flash('Ваш аккаунт был создан!', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html', title='Регистрация', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('main.dashboard_teacher'))
        elif current_user.role == 'student':
            return redirect(url_for('main.dashboard_student'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or url_for('main.login') in next_page or url_for('main.register') in next_page:
                if user.role == 'teacher':
                    next_page = url_for('main.dashboard_teacher')
                elif user.role == 'student':
                    next_page = url_for('main.dashboard_student')
            return redirect(next_page)
        else:
            flash('Не удалось войти. Пожалуйста, проверьте электронную почту и пароль', 'danger')
    return render_template('login.html', title='Вход', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/dashboard/teacher")
@login_required
def dashboard_teacher():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    student_count_by_form = db.session.query(Student.education_form, db.func.count(Student.id)).group_by(Student.education_form).all()
    return render_template('dashboard_teacher.html', student_count_by_form=student_count_by_form)

@main.route("/dashboard/student")
@login_required
def dashboard_student():
    if current_user.role != 'student':
        return redirect(url_for('main.home'))
    student = Student.query.filter_by(user_id=current_user.id).first()
    if student is None:
        flash('Студент не найден.', 'danger')
        return redirect(url_for('main.home'))
    grades = Grade.query.filter_by(student_id=student.id).all()
    subjects = {grade.subject_id: Subject.query.get(grade.subject_id) for grade in grades}
    return render_template('dashboard_student.html', student=student, grades=grades, subjects=subjects)

@main.route("/teacher/manage_students", methods=['GET', 'POST'])
@login_required
def manage_students():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, admission_year=form.admission_year.data,
                          education_form=form.education_form.data, group_name=form.group_name.data, user_id=form.user_id.data)
        db.session.add(student)
        db.session.commit()
        flash('Студент добавлен!', 'success')
        return redirect(url_for('main.manage_students'))
    return render_template('manage_students.html', form=form)

@main.route("/teacher/manage_subjects", methods=['GET', 'POST'])
@login_required
def manage_subjects():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, semester=form.semester.data, hours=form.hours.data, assessment_type=form.assessment_type.data)
        db.session.add(subject)
        db.session.commit()
        flash('Предмет добавлен!', 'success')
        return redirect(url_for('main.manage_subjects'))
    return render_template('manage_subjects.html', form=form)

@main.route("/teacher/manage_grades", methods=['GET', 'POST'])
@login_required
def manage_grades():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade(year=form.year.data, semester=form.semester.data, student_id=form.student_id.data, subject_id=form.subject_id.data, grade=form.grade.data)
        db.session.add(grade)
        db.session.commit()
        flash('Оценка добавлена!', 'success')
        return redirect(url_for('main.manage_grades'))
    return render_template('manage_grades.html', form=form)
