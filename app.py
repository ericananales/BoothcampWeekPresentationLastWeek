from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret"

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Menu encoding
MENU_CODE = {
    "Burger": 0,
    "Pasta": 1,
    "Salad": 2,
    "Pizza": 3,
    "Ramen": 4,
    "Sandwich": 5,
    "Rice Meal": 6,
    "Fries": 7
}

# Create DB if not exists
def init_db():
    if not os.path.exists('orders.db'):
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu TEXT,
                quantity INTEGER,
                time_of_day INTEGER,
                kitchen_load INTEGER,
                predicted_wait_time REAL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            menu_items = request.form.getlist("menu_item[]")
            num_items = list(map(int, request.form.getlist("num_items[]")))
            time_of_day = int(request.form["time_of_day"])
            kitchen_load = int(request.form["kitchen_load"])

            predictions = []
            conn = sqlite3.connect('orders.db')
            c = conn.cursor()

            for i in range(len(menu_items)):
                menu = menu_items[i]
                qty = num_items[i]
                code = MENU_CODE[menu]

                wait_time = model.predict([[code, qty, time_of_day, kitchen_load]])[0]
                predictions.append(f"📝 {menu} x{qty} → ⏳ {round(wait_time, 1)} mins")

                c.execute("INSERT INTO orders (menu, quantity, time_of_day, kitchen_load, predicted_wait_time) VALUES (?, ?, ?, ?, ?)",
                          (menu, qty, time_of_day, kitchen_load, wait_time))

            conn.commit()
            conn.close()

            session['result'] = "<br>".join(predictions)

        except Exception as e:
            session['result'] = f"⚠️ Error: {e}"

        return redirect(url_for('index'))

    result = session.pop('result', None)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
