from flask import Flask, render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

from loginform import LoginForm
from data import db_session
from data.users import User
from data.events import Event
from data.courses import Course

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"

USERS = {"Alex": "123456"}
user2 = ""


@app.route("/")
def index():
    if user2 == "":
        return redirect('/sign_in')
    db_sess = db_session.create_session()
    data = {"title": "Главная страница",
            "events": db_sess.query(Event)
            }
    return render_template("index.html", **data)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data in USERS:
            if form.password.data == USERS[form.username.data]:
                global user2
                user2 = form.username.data
                return redirect('/user_page')
            else:
                flash("Пароль неверный.")
        else:
            flash("Такого пользователя не существует.")
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route("/user_page")
def user_page():
    data = {"username": user2, "title": "Страница пользователя"}
    return render_template("user_page.html", **data)


@app.route("/exit_lk")
def exit_lk():
    global user2
    user2 = ""
    return redirect('/')


if __name__ == "__main__":
    db_session.global_init("db/report_tch.db")

    # db_sess = db_session.create_session()

    # user = User()
    # user.name = "Попов Александр Степанович"
    # user.login = "popov"
    # user.email = "admin@tch_mail.ru"
    # user.hashed_password = "123456"
    # user.admin = True
    # user2 = User()
    # user2.name = "Глушков Виктор Михайлович"
    # user2.login = "glush"
    # user2.email = "glush@tch_mail.ru"
    # user2.hashed_password = "123456"
    # user3 = User()
    # user3.name = "Котельников Владимир Александрович"
    # user3.login = "kotel"
    # user3.email = "kotel@tch_mail.ru"
    # user3.hashed_password = "123456"
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

    # db_sess.commit()

    # ----- view db --------
    # for user in db_sess.query(User).all():
    #     print(user)
    # print()
    # for course in db_sess.query(Course).all():
    #     print(course)

    app.run(debug=True)
