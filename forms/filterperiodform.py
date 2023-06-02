from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FilterPeriodForm(FlaskForm):
    title = SelectField('Выберите период', choices=[])
    submit = SubmitField('Фильтровать')
