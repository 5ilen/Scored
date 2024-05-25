from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models.models import User, Student, Subject

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=50, message='Имя пользователя должно быть от 3 до 50 символов.')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат email.')])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, message='Пароль должен быть не менее 6 символов.')])
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
    student_id = SelectField('Студент', coerce=int, validators=[DataRequired()])  # Используем SelectField для выбора студента
    subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired()])  # Используем SelectField для выбора предмета
    grade = StringField('Оценка', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(student.id, student.name) for student in Student.query.all()]
        self.subject_id.choices = [(subject.id, subject.name) for subject in Subject.query.all()]