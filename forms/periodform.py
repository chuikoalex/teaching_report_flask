from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


class PeriodForm(FlaskForm):
    title = StringField('Название периода (выводится перед списком мероприятий)', validators=[DataRequired()])
    date_start = DateField("Дата начала периода(список формируется начиная с этой даты)",
                           format='%Y-%m-%d', validators=[DataRequired()])
    date_end = DateField("Дата окончания периода (до этой даты не включительно)",
                         format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Добавить период')
