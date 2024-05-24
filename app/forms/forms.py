from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.models import User
from email_validator import validate_email, EmailNotValidError

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Это поле обязательно для заполнения.'),
        Length(min=2, max=20, message='Имя пользователя должно быть от 2 до 20 символов.')
    ])
    email = StringField('Электронная почта', validators=[
        DataRequired(message='Это поле обязательно для заполнения.')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Это поле обязательно для заполнения.')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Это поле обязательно для заполнения.'),
        EqualTo('password', message='Пароли должны совпадать.')
    ])
    role = SelectField('Роль', choices=[('student', 'Студент'), ('teacher', 'Преподаватель')], validators=[
        DataRequired(message='Это поле обязательно для заполнения.')
    ])
    access_code = StringField('Код доступа (для преподавателей)')
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        try:
            validate_email(email.data)
        except EmailNotValidError as e:
            raise ValidationError('Некорректный адрес электронной почты.')

    def validate_access_code(self, access_code):
        if self.role.data == 'teacher' and access_code.data != '1':
            raise ValidationError('Неверный код доступа для преподавателей.')

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[
        DataRequired(message='Это поле обязательно для заполнения.'),
        Email(message='Некорректный адрес электронной почты.')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Это поле обязательно для заполнения.')
    ])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
