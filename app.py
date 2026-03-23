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

@app.route("/loop")
def loop():
    data = ["Python", "Flask", "HTML", "CSS", "VScode"]
    return render_template("loop.html", items=data)

@app.route("/dictators")
def dictators():
    dictators = [{"name": "Netanyahu",
                  "status": "alive",
                  "body_count": "over 50000",
                  "country": "Country placed in Palestine"},
                  {"name": "Adolf",
                  "status": "unknown",
                  "body_count": "a lot",
                  "country": "Fur Deutschland"},
                  {"name": "Donald T",
                  "status": "agent",
                  "body_count": "idk",
                  "country": "Fur Deutschland"}
                 ]
    return render_template("dictators.html", dictators=dictators)

app.run(debug=True)