from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    title = StringField('Заголовок')
    type_event = SelectField('Тип мероприятия',
                             choices=["Конкурс", "Семинар", "Соревнование", "Игра", "Экскурсия"])
    date_start = DateField("Дата начала (по умолчанию 'сегодня')", format='%Y-%m-%d')
    date_end = DateField("Дата окончания (если длилось несколько дней)", format='%Y-%m-%d')
    members = IntegerField('Количество участников')
    content = TextAreaField('Содержание')
    course_id = SelectField('Курс/объединение')
    submit = SubmitField('Добавить')
