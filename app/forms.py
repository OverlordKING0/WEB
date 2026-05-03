from sqlalchemy import Boolean
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.fields.simple import BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_wtf import FlaskForm


class NewsForm(FlaskForm):
    title = StringField('Название',
                        validators=[DataRequired(message='Поле не должно быть пустым'),
                                    Length(max=255, message='Заголовок новости не может превышать 256 символов')])
    text = TextAreaField(
        'Опишите новость:',
        validators=[DataRequired(message='Поле не должно быть пустым')])
    category = SelectField('Категория', choices=[])
    button = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        from .models import Category
        categories = Category.query.all()
        self.category.choices = [(category.id, category.title) for category in categories]

class LoginForm(FlaskForm):
    username = StringField('Имя Пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired(), Email(message='Некорректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')