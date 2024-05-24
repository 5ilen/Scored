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

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class StudentForm(FlaskForm):
    name = StringField('Имя студента', validators=[DataRequired()])
    admission_year = IntegerField('Год поступления', validators=[DataRequired()])
    education_form = SelectField('Форма обучения', choices=[('day', 'Дневная'), ('evening', 'Вечерняя'), ('distance', 'Дистанционная')], validators=[DataRequired()])
    group_name = StringField('Группа', validators=[DataRequired()])
    user_id = IntegerField('ID пользователя', validators=[DataRequired()])
    submit = SubmitField('Добавить студента')

class SubjectForm(FlaskForm):
    name = StringField('Название предмета', validators=[DataRequired()])
    semester = IntegerField('Семестр', validators=[DataRequired()])
    hours = IntegerField('Количество часов', validators=[DataRequired()])
    assessment_type = SelectField('Тип оценки', choices=[('exam', 'Экзамен'), ('credit', 'Зачет')], validators=[DataRequired()])
    submit = SubmitField('Добавить предмет')

class GradeForm(FlaskForm):
    year = IntegerField('Год', validators=[DataRequired()])
    semester = IntegerField('Семестр', validators=[DataRequired()])
    student_id = IntegerField('ID студента', validators=[DataRequired()])
    subject_id = IntegerField('ID предмета', validators=[DataRequired()])
    grade = StringField('Оценка', validators=[DataRequired()])
    submit = SubmitField('Добавить оценку')
