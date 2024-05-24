from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.forms.forms import RegistrationForm, LoginForm
from app.models.models import User, Student, Subject, Grade
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == 'teacher' and form.access_code.data != '1':
            flash('Неверный код доступа для преподавателей', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash('Ваш аккаунт был создан!', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html', title='Регистрация', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Не удалось войти. Пожалуйста, проверьте электронную почту и пароль', 'danger')
    return render_template('login.html', title='Вход', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == 'teacher':
        return render_template('dashboard_teacher.html')
    elif current_user.role == 'student':
        return render_template('dashboard_student.html')
    return redirect(url_for('main.home'))
