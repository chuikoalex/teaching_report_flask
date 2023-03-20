from flask import Flask, url_for, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from loginform import LoginForm
from registerform import RegisterForm
from eventform import EventForm
from data import db_session
from data.users import User
from data.events import Event
from data.courses import Course

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))
    db_sess = db_session.create_session()
    data = {"title": "Главная страница",
            "events": db_sess.query(Event)
            }
    return render_template("index.html", **data)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
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
def reqister():
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
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/user_page")
def user_page():
    data = {"title": "Страница пользователя"}
    return render_template("user_page.html", **data)


@app.route("/function", methods=['GET', 'POST'])
def function():
    if not current_user.is_authenticated:
        return redirect(url_for('sign_in'))

    db_sess = db_session.create_session()
    form = EventForm()
    if request.method == "POST":
        if form.title.data != "":
            event = Event()
            event.title = form.title.data
            if form.date_start.data is not None:
                event.start_date = form.date_start.data
                event.end_date = form.date_start.data
            if form.date_end.data is not None:
                event.end_date = form.date_end.data
            event.type_event = form.type_event.data
            event.members = form.members.data
            event.content = form.content.data
            current_user.events.append(event)
            db_sess.merge(current_user)
            db_sess.commit()
        else:
            flash("Необходимо заполнить поле Заголовок")
        return redirect('/function')

    data = {"title": "Главная страница",
            "form": form
            }
    return render_template("function.html", **data)


@app.route("/exit_lk")
def exit_lk():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    db_session.global_init("db/report_tch.db")
    app.run(debug=True)


