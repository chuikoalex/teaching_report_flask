import datetime

from flask import Flask, url_for, render_template, request, redirect, flash, send_file
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.eventform import EventForm
from forms.periodform import PeriodForm
from forms.filterperiodform import FilterPeriodForm
from data import db_session
from data.users import User
from data.events import Event
from data.periods import Period
# from data.courses import Course

from openpyxl import Workbook
from tempfile import NamedTemporaryFile

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = FilterPeriodForm()
    now_date = datetime.datetime.now()
    periods = db_sess.query(Period).order_by(Period.title.desc()).all()
    form.title.choices = [per.title for per in periods]

    if request.method == "POST":
        period_filter = db_sess.query(Period).filter(Period.title == form.title.data).first()
        return redirect(f'/{period_filter.id}')

    period = db_sess.query(Period).filter(Period.start_date <= now_date).filter(Period.end_date > now_date).first()
    if not period:
        period = db_sess.query(Period).first()
    if period:
        period_title = period.title
        events = db_sess.query(Event).filter(
            Event.start_date >= period.start_date).filter(
            Event.start_date < period.end_date).order_by(
            Event.start_date.desc()).all()
    else:
        period_title = "<ошибка> отсутствуют периоды"
        events = []

    data = {"title": "Главная страница",
            "period_title": period_title,
            "form": form,
            "events": events,
            }
    return render_template("index.html", **data)


@app.route("/<int:period_id>",  methods=['GET', 'POST'])
def index_filter(period_id):
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = FilterPeriodForm()
    periods = db_sess.query(Period).order_by(Period.title.desc()).all()

    form.title.choices = [per.title for per in periods]
    period = db_sess.query(Period).filter(Period.id == period_id).first()

    if request.method == "POST":
        period_filter = db_sess.query(Period).filter(Period.title == form.title.data).first()
        return redirect(f'/{period_filter.id}')

    if not period:
        redirect("/")
    period_title = period.title
    events = db_sess.query(Event).filter(
        Event.start_date >= period.start_date).filter(
        Event.start_date < period.end_date).order_by(
        Event.start_date.desc()).all()

    data = {"title": "Главная страница",
            "period_title": period_title,
            "form": form,
            "events": events,
            }
    return render_template("index.html", **data)


@app.route('/export_to_file/<period_title>')
def export_to_file(period_title):
    db_sess = db_session.create_session()
    period = db_sess.query(Period).filter(Period.title == period_title).first()
    events = db_sess.query(Event).filter(
        Event.start_date >= period.start_date).filter(
        Event.start_date < period.end_date).order_by(
        Event.start_date.desc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Данные"
    ws['A1'] = period_title
    ws.append(["Пользователь",
               "Название",
               "Тип",
               "Уровень",
               "Дата начала",
               "Дата окончания",
               "Количество участников",
               "Описание",
               ])
    for event in events:
        event: Event()
        user = db_sess.query(User).filter(User.id == event.user_id).first()
        ws.append([user.name,
                   event.title,
                   event.type_event,
                   event.level_event,
                   event.start_date,
                   event.end_date,
                   event.members,
                   event.content,
                   ])

    tmp = NamedTemporaryFile().name
    wb.save(tmp)
    return send_file(tmp, as_attachment=True, download_name="export_data.xlsx")


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.login == form.login.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            else:
                flash("Логин и/или пароль неверны!")
        else:
            flash("Поля не могут быть пустыми!")
        return redirect(url_for('sign_in'))
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated or not current_user.admin:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == form.login.data).first():
                flash("Такой пользователь уже существует!")
                return redirect('/register')
            if db_sess.query(User).filter(User.email == form.email.data).first():
                flash("Такая почта уже есть в базе данных!")
                return redirect('/register')
            if form.password.data != form.password_again.data:
                flash("Пароли не совпадают!")
                return redirect('/register')
            user = User()
            user.login = form.login.data
            user.name = form.name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            flash("oK")
            return redirect('/register')
    data = {"title": "Регистрация",
            "users": db_sess.query(User).order_by(User.name).all(),
            "form": form,
            }
    return render_template('register.html', **data)


@app.route('/period', methods=['GET', 'POST'])
@app.route('/period/<int:period_id>', methods=['GET', 'POST'])
def period(period_id=-1):
    if not current_user.is_authenticated or not current_user.admin:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = PeriodForm()

    if request.method == "GET" and period_id != -1:
        period = db_sess.query(Period).filter(Period.id == period_id).first()
        if period:
            form.title.data = period.title
            form.date_start.data = period.start_date
            form.date_end.data = period.end_date
            form.submit.label.text = "Изменить"

    if request.method == "POST":
        if form.validate_on_submit():
            if form.date_start.data is None or form.date_end.data is None:
                flash("Наличие даты начала и окончания обязательны!")
                return redirect('/period')
            if not form.date_start.data < form.date_end.data:
                flash("Дата начала периода, должна быть меньше!")
                return redirect('/period')
            db_sess = db_session.create_session()
            if period_id == -1:
                period = Period()
            else:
                period = db_sess.query(Period).filter(Period.id == period_id).first()
            if period:
                period.title = form.title.data
                period.start_date = form.date_start.data
                period.end_date = form.date_end.data
                if period_id == -1:
                    db_sess.add(period)
                db_sess.commit()
                flash("oK")
            return redirect('/period')

    data = {"title": "Периоды",
            "periods": db_sess.query(Period).order_by(Period.start_date.desc()).all(),
            "form": form,
            }
    return render_template('period.html', **data)


@app.route('/period_delete/<int:period_id>', methods=['GET', 'POST'])
@login_required
def period_delete(period_id):
    if not current_user.is_authenticated or not current_user.admin:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    period = db_sess.query(Period).filter(Period.id == period_id).first()
    if period:
        db_sess.delete(period)
        db_sess.commit()
    return redirect('/period')


@app.route("/user_page")
@login_required
def user_page():
    data = {"title": "Страница пользователя"}
    return render_template("user_page.html", **data)


@app.route("/function", methods=['GET', 'POST'])
@login_manager.user_loader
def function():
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = EventForm()
    if request.method == "POST":
        if form.title.data.strip() != "":
            db_sess = db_session.create_session()
            event = Event()
            event.title = form.title.data
            if form.date_start.data is not None:
                event.start_date = form.date_start.data
                event.end_date = form.date_start.data
            if form.date_end.data is not None:
                event.end_date = form.date_end.data
            event.type_event = form.type_event.data
            event.level_event = form.level_event.data
            event.members = form.members.data
            event.content = form.content.data
            current_user.events.append(event)
            db_sess.merge(current_user)
            db_sess.commit()
        return redirect('/function')
    data = {"title": "Функционал",
            "form": form,
            "events": db_sess.query(Event).filter(Event.user == current_user).order_by(Event.start_date.desc()).all(),
            }
    return render_template("function.html", **data)


@app.route('/function/<int:event_id>', methods=['GET', 'POST'])
@login_required
@login_manager.user_loader
def edit_events(event_id):
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    form = EventForm()
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == event_id, Event.user == current_user).first()
    if event:
        if request.method == "GET":
            form.title.data = event.title
            form.date_start.data = event.start_date
            form.date_end.data = event.end_date
            form.type_event.data = event.type_event
            form.level_event.data = event.level_event
            form.members.data = event.members
            form.content.data = event.content
            form.submit.label.text = "Изменить"

        if request.method == "POST":
            if form.title.data.strip() != "":
                event.title = form.title.data
                if form.date_start.data is not None:
                    event.start_date = form.date_start.data
                    event.end_date = form.date_start.data
                if form.date_end.data is not None:
                    event.end_date = form.date_end.data
                event.type_event = form.type_event.data
                event.level_event = form.level_event.data
                event.members = form.members.data
                event.content = form.content.data
                db_sess.commit()
                return redirect('/function')
    else:
        return redirect('/function')
    data = {"title": "Редактирование мероприятия",
            "form": form,
            "events": [event],
            }
    return render_template("function.html", **data)


@app.route('/event_delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_delete(event_id):
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == event_id, Event.user == current_user).first()
    if event:
        db_sess.delete(event)
        db_sess.commit()
    return redirect('/function')


@app.route("/exit_lk")
def exit_lk():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == "__main__":
    db_session.global_init("db/report_tch.db")
    app.run(debug=True)
