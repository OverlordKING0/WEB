from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired
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