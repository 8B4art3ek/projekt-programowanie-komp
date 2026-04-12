from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simple_form", methods=["GET", "POST"])
def simple_form():
    dictatorName = None
    error = None
    if request.method == "POST":
        dictatorName = request.form.get("dictatorName")
        if not dictatorName or not dictatorName.strip():
            dictatorName = None
            error = "Brak nazwy dyktatora"
    return render_template("simple_form.html", dictatorName=dictatorName, error=error)


@app.route("/calc", methods=["GET", "POST"])
def calc():
    result = None
    error = None
    a_str = None
    b_str = None
    operator = None

    if request.method == "POST":
        a_str = request.form.get("a")
        b_str = request.form.get("b")
        operator = request.form.get("operator")

        # 1. Sprawdzamy czy cokolwiek wpisano
        if not a_str or not b_str:
            error = "Podaj obie liczby"
            return render_template("calc.html", result=None, error=error, a=a_str, b=b_str, operator=operator)
        
        # 2. Rzutowanie na float (zabezpieczenie przed wpisaniem tekstu np. "cebula")
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            error = "Podano błędne wartości, wpisz liczby!"
            return render_template("calc.html", result=None, error=error, a=a_str, b=b_str, operator=operator)
        
        # 3. Zabezpieczenie przed dzieleniem przez zero
        if operator == "/" and b == '0':
            error = "Nie wolno dzielić przez 0!"
            return render_template("calc.html", result=None, error=error, a=a_str, b=b_str, operator=operator)
        
        # 4. Liczenie
        if operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == "*":
            result = a * b
        elif operator == "/":
            result = a / b
        else:
            error = "Nieznany operator"

        # Opcjonalnie: ucinanie .0 na końcu, żeby liczby całkowite ładniej wyglądały (np. 5 zamiast 5.0)
        if result is not None and result.is_integer():
            result = int(result)

    return render_template("calc.html", result=result, error=error, a=a_str, b=b_str, operator=operator)

app.run(debug=True)