from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

@app.route("/about")
def about():
    return "O nas"

@app.route("/contact")
def contact():
    return "Kontakt"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}"

@app.route("/square/<int:n>")
def square(n):
    return f"Kwadrat liczby {n} to: {n**2}"

from datetime import datetime
@app.route("/time")
def time():
    return f"Aktualny czas serwera: {datetime.now()}"

from flask import render_template
@app.route("/hello_template/<nickname>")
def hello_template(nickname):
    return render_template("hello.html", name=nickname)

@app.route("/age/<int:age>")
def age(age):
    return render_template("age.html", age=age)

app.run(debug=True)