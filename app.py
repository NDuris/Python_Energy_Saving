from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_FILE = "energy_data.db"

def query_energy_data(days=30):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT Date, Hour, SpotPriceDKK
        FROM energy
        WHERE Date >= date('now', ? || ' days')
        ORDER BY Date ASC, Hour ASC
    """, (f"-{days}",))
    rows = [{"date": r[0], "hour": r[1], "spot_price_dkk": r[2]} for r in c.fetchall()]
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def index():
    days = 30
    if request.method == "POST":
        try:
            days = int(request.form.get("days", 30))
        except ValueError:
            days = 30
        days = max(1, min(days, 30))

    data = query_energy_data(days)
    return render_template("index.html", data=data, days=days)

if __name__ == "__main__":
    app.run(debug=True)
