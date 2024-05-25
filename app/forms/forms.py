from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Роль', choices=[('student', 'Студент'), ('teacher', 'Преподаватель')], validators=[DataRequired()])
    access_code = StringField('Код доступа (только для преподавателей)')
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот адрес электронной почты уже используется. Пожалуйста, выберите другой.')

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class EducationForm(FlaskForm):
    education_form = SelectField('Форма обучения', choices=[('дневная', 'Дневная'), ('вечерняя', 'Вечерняя'), ('заочная', 'Заочная')], validators=[DataRequired()])
    submit = SubmitField('Посчитать студентов')
class StudentForm(FlaskForm):
    name = StringField('ФИО студента', validators=[DataRequired()])
    admission_year = IntegerField('Год поступления', validators=[DataRequired()])
    education_form = SelectField('Форма обучения', choices=[('дневная', 'Дневная'), ('вечерняя', 'Вечерняя'), ('заочная', 'Заочная')], validators=[DataRequired()])
    group_name = StringField('Номер группы', validators=[DataRequired()])
    user_id = IntegerField('ID пользователя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class SubjectForm(FlaskForm):
    name = StringField('Название дисциплины', validators=[DataRequired()])
    semester = IntegerField('Семестр', validators=[DataRequired()])
    hours = IntegerField('Количество часов', validators=[DataRequired()])
    assessment_type = StringField('Форма отчетности', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class GradeForm(FlaskForm):
    year = IntegerField('Год', validators=[DataRequired()])
    semester = IntegerField('Семестр', validators=[DataRequired()])
    student_id = IntegerField('ID студента', validators=[DataRequired()])
    subject_id = IntegerField('ID предмета', validators=[DataRequired()])
    grade = StringField('Оценка', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
