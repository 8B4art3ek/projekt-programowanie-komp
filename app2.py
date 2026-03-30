from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask działa"

@app.route("/simple_form", methods=["GET", "POST"])
def simple_form():
    dictatorName = None
    error = None
    if request.method == "POST":
        dictatorName = request.form.get("dictatorName")
        if not dictatorName.strip():
            dictatorName = None
            error = "Brak nazwy dyktatora"
    return render_template("simple_form.html", dictatorName=dictatorName, error=error)

@app.route("/calc", methods=["GET", "POST"])
def calc():
    result = None
    error = None
    a = None
    b = None
    operator = None
    if request.method == "POST":
        a = request.form.get("a")
        b = request.form.get("b")
        operator = request.form.get("operator")
        if not a or not b:
            error = "Podaj obie liczby"
            return render_template("calc.html", result=None, error=error, a=a, b=b, operator=operator)
        if operator == "/" and b == '0':
            error = "Nie wolno dzielić przez 0!"
            return render_template("calc.html", result=None, error=error, a=a, b=b, operator=operator)
        result = eval(f"{a}{operator}{b}")
    return render_template("calc.html", result=result, error=error, a=a, b=b, operator=operator)
app.run(debug=True)