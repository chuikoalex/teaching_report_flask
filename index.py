from flask import Flask, url_for, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from loginform import LoginForm
from registerform import RegisterForm
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
            "username": session['username'],
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
                flash("Логин и/или пароль не верны!")
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
            return redirect(url_for('sign_in'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/user_page")
def user_page():
    data = {"username": session['username'], "title": "Страница пользователя"}
    return render_template("user_page.html", **data)


@app.route("/exit_lk")
def exit_lk():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == "__main__":
    db_session.global_init("db/report_tch.db")
    app.run(debug=True)

    # db_session.global_init("db/report_tch.db")

    # app.run(debug=True)
    # login_manager = LoginManager()
    # login_manager.init_app(app)

    # db_sess = db_session.create_session()

    # user = User()
    # user.name = "Попов Александр Степанович"
    # user.login = "popov"
    # user.email = "admin@email.ru"
    # user.admin = True
    # user.set_password("123456")
    # user2 = User()
    # user2.name = "Глушков Виктор Михайлович"
    # user2.login = "glush"
    # user2.email = "glush@email.ru"
    # user2.set_password("123456")
    # user3 = User()
    # user3.name = "Котельников Владимир Александрович"
    # user3.login = "kotel"
    # user3.email = "kotel@email.ru"
    # user3.set_password("kotel@email.ru")
    # db_sess.add(user)
    # db_sess.add(user2)
    # db_sess.add(user3)

    # course = Course(title="Программирование", user_id=1)
    # course1 = Course(title="Радиолюбитель", user_id=1)
    # course2 = Course(title="Робототехника")
    # course3 = Course(title="Основы криптографии", user_id=3)
    # course4 = Course(title="Основы кибернетики", user_id=2)
    # db_sess.add(course)
    # db_sess.add(course1)
    # db_sess.add(course2)
    # db_sess.add(course3)
    # db_sess.add(course4)

    # event = Event(title="Конкурс самых лучших радиолюбителей.",
    #               type_event="Конкурс",
    #               members="5",
    #               content="Мы участвовали в конкурсе и даже смогли занять второе место с конца! Ура мы молодцы!!!",
    #               course_id=1,
    #               user_id=1)
    # event2 = Event(title="Семинар << Стремительное развитие IT-сферы >>.",
    #                type_event="Семинар",
    #                members="12",
    #                content="Участие группы Основы кибернетики в региональном онлайн-семинаре. "
    #                        "Нового особо ни чего не было, мы и так все знаем.",
    #                course_id=5,
    #                user_id=2)
    # event3 = Event(title="Экскурсия в несекретные отделы Администрации района.",
    #                type_event="Экскурсия",
    #                members="8",
    #                content="Нас тут особо не ждали, но мы показали как нужно правильно шифровать ПД.",
    #                course_id=4,
    #                user_id=3)
    # db_sess.add(event)
    # db_sess.add(event2)
    # db_sess.add(event3)
    #
    # db_sess.commit()

    # for user in db_sess.query(User).all():
    #     print(user)
    #     print("Password:", user.check_password("123456"))
    # print()
    # for course in db_sess.query(Course).all():
    #     print(course)
