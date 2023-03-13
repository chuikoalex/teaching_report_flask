from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"

user = "Alex"
password = "123456"


@app.route("/")
def index():
    data = {"username": user, "title": "Главная страница"}
    return render_template("index.html", **data)


if __name__ == "__main__":
    app.run(debug=True)
