from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    title = StringField('Заголовок (обязателен для заполнения)', validators=[DataRequired()])
    type_event = SelectField('Тип мероприятия',
                             choices=["Вебинар",
                                      "Выставка",
                                      "Занятие",
                                      "Игра",
                                      "Конкурс",
                                      "Конференция",
                                      "Круглый стол",
                                      "Мастер-класс",
                                      "Проект",
                                      "Семинар",
                                      "Соревнование",
                                      "Тренинг",
                                      "Фестиваль",
                                      "Форум",
                                      "Экскурсия",
                                      "ДРУГОЕ",
                                      ])
    level_event = SelectField('Уровень мероприятия',
                              choices=["Школьный",
                                       "Муниципальный",
                                       "Районный",
                                       "Городской",
                                       "Региональный",
                                       "Межрегиональный",
                                       "Всероссийский",
                                       "Международный",
                                       ])
    date_start = DateField("Дата начала (если поле оставить пустым будет установлена сегодняшняя дата)",
                           format='%Y-%m-%d')
    date_end = DateField("Дата окончания (если длилось несколько дней)",
                         format='%Y-%m-%d')
    members = IntegerField('Количество участников', default=1)
    content = TextAreaField('Описание мероприятия')
    course_id = SelectField('Курс/объединение')
    submit = SubmitField('Добавить')
