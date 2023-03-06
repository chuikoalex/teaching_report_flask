from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = "my mega secret key"


@app.route("/")
def index():
    data = {"username": "Alex", "title": "Главная страница"}
    return render_template("index.html", **data)


if __name__ == "__main__":
    app.run(debug=True)
