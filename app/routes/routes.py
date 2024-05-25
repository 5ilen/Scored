from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.forms.forms import RegistrationForm, LoginForm, StudentForm, SubjectForm, GradeForm, EducationForm
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        if form.role.data == 'student':
            student = Student(name=form.username.data, admission_year=datetime.now().year, 
                              education_form='day', group_name='default', user_id=user.id)
            db.session.add(student)
            db.session.commit()

        flash('Ваш аккаунт был создан! Вы можете войти в систему', 'success')
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

@main.route("/dashboard_teacher")
@login_required
def dashboard_teacher():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    
    student_count_by_form = db.session.query(
        Student.education_form, db.func.count(Student.id)
    ).group_by(Student.education_form).all()
    
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

@main.route("/students/count", methods=['GET', 'POST'])
@login_required
def count_students():
    form = EducationForm()
    count = None
    if form.validate_on_submit():
        count = Student.query.filter_by(education_form=form.education_form.data).count()
    return render_template('count_students.html', form=form, count=count)

@main.route("/subject/info", methods=['GET', 'POST'])
@login_required
def subject_info():
    form = SubjectForm()
    info = None
    if form.validate_on_submit():
        subject = Subject.query.filter_by(name=form.name.data).first()
        if subject:
            info = {'hours': subject.hours, 'assessment_type': subject.assessment_type}
    return render_template('subject_info.html', form=form, info=info)

@main.route("/student/add", methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        try:
            student = Student(
                name=form.name.data,
                admission_year=form.admission_year.data,
                education_form=form.education_form.data,
                group_name=form.group_name.data,
                user_id=current_user.id
            )
            db.session.add(student)
            db.session.commit()
            flash('Студент добавлен!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении студента: {str(e)}', 'danger')
    return render_template('add_student.html', title='Добавить студента', form=form)

@main.route("/student/edit/<int:student_id>", methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm()
    if form.validate_on_submit():
        try:
            student.name = form.name.data
            student.admission_year = form.admission_year.data
            student.education_form = form.education_form.data
            student.group_name = form.group_name.data
            db.session.commit()
            flash('Информация о студенте обновлена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при редактировании студента: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.name.data = student.name
        form.admission_year.data = student.admission_year
        form.education_form.data = student.education_form
        form.group_name.data = student.group_name
    return render_template('edit_student.html', title='Редактировать студента', form=form)

@main.route("/subject/add", methods=['GET', 'POST'])
@login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        try:
            subject = Subject(
                name=form.name.data,
                semester=form.semester.data,
                hours=form.hours.data,
                assessment_type=form.assessment_type.data
            )
            db.session.add(subject)
            db.session.commit()
            flash('Дисциплина добавлена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении дисциплины: {str(e)}', 'danger')
    return render_template('add_subject.html', title='Добавить дисциплину', form=form)

@main.route("/subject/edit/<int:subject_id>", methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm()
    if form.validate_on_submit():
        try:
            subject.name = form.name.data
            subject.semester = form.semester.data
            subject.hours = form.hours.data
            subject.assessment_type = form.assessment_type.data
            db.session.commit()
            flash('Информация о дисциплине обновлена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при редактировании дисциплины: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.name.data = subject.name
        form.semester.data = subject.semester
        form.hours.data = subject.hours
        form.assessment_type.data = subject.assessment_type
    return render_template('edit_subject.html', title='Редактировать дисциплину', form=form)

@main.route("/grade/add", methods=['GET', 'POST'])
@login_required
def add_grade():
    form = GradeForm()
    if form.validate_on_submit():
        try:
            grade = Grade(
                year=form.year.data,
                semester=form.semester.data,
                student_id=form.student_id.data,
                subject_id=form.subject_id.data,
                grade=form.grade.data
            )
            db.session.add(grade)
            db.session.commit()
            flash('Оценка добавлена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении оценки: {str(e)}', 'danger')
    return render_template('add_grade.html', title='Добавить оценку', form=form)

@main.route("/grade/edit/<int:grade_id>", methods=['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    form = GradeForm()
    if form.validate_on_submit():
        try:
            grade.year = form.year.data
            grade.semester = form.semester.data
            grade.student_id = form.student_id.data
            grade.subject_id = form.subject_id.data
            grade.grade = form.grade.data
            db.session.commit()
            flash('Оценка обновлена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при редактировании оценки: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.year.data = grade.year
        form.semester.data = grade.semester
        form.student_id.data = grade.student_id
        form.subject_id.data = grade.subject_id
        form.grade.data = grade.grade
    return render_template('edit_grade.html', title='Редактировать оценку', form=form)

@main.route("/students/manage", methods=['GET'])
@login_required
def manage_students():
    sort_by = request.args.get('sort_by', 'name')
    filter_by = request.args.get('filter_by', '')
    students = Student.query
    if filter_by:
        students = students.filter(Student.name.contains(filter_by))
    students = students.order_by(sort_by).all()
    return render_template('manage_students.html', title='Управление студентами', students=students, sort_by=sort_by, filter_by=filter_by)

@main.route("/subjects/manage", methods=['GET'])
@login_required
def manage_subjects():
    sort_by = request.args.get('sort_by', 'name')
    filter_by = request.args.get('filter_by', '')
    subjects = Subject.query
    if filter_by:
        subjects = subjects.filter(Subject.name.contains(filter_by))
    subjects = subjects.order_by(sort_by).all()
    return render_template('manage_subjects.html', title='Управление предметами', subjects=subjects, sort_by=sort_by, filter_by=filter_by)

@main.route("/grades/manage", methods=['GET'])
@login_required
def manage_grades():
    sort_by = request.args.get('sort_by', 'grade')
    filter_by = request.args.get('filter_by', '')
    grades = Grade.query
    if filter_by:
        grades = grades.join(Student).filter(Student.name.contains(filter_by))
    grades = grades.order_by(sort_by).all()
    return render_template('manage_grades.html', title='Управление оценками', grades=grades, sort_by=sort_by, filter_by=filter_by)