from flask import Flask, render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

from loginform import LoginForm
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"

USERS = {"Alex": "123456"}
user = ""


@app.route("/")
def index():
    if user == "":
        return redirect('/sign_in')
    data = {"username": user, "title": "Главная страница"}
    return render_template("index.html", **data)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data in USERS:
            if form.password.data == USERS[form.username.data]:
                global user
                user = form.username.data
                return redirect('/user_page')
            else:
                flash("Пароль неверный.")
        else:
            flash("Такого пользователя не существует.")
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route("/user_page")
def user_page():
    data = {"username": user, "title": "Страница пользователя"}
    return render_template("user_page.html", **data)


@app.route("/exit_lk")
def exit_lk():
    global user
    user = ""
    return redirect('/')


if __name__ == "__main__":
    db_session.global_init("db/report_tch.db")
    app.run(debug=True)
