from flask import Flask, render_template, request, send_file
import sqlite3
import io
import csv
from datetime import datetime

app = Flask(__name__)
DB_FILE = "energy_data.db"

def query_energy_data(start_date=None, end_date=None):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = "SELECT Date, Hour, SpotPriceDKK FROM energy"
    params = []

    if start_date and end_date:
        query += " WHERE Date BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    query += " ORDER BY Date ASC, Hour ASC"
    c.execute(query, params)
    
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def table_view():
    start = end = None
    if request.method == "POST":
        start = request.form.get("start_date")
        end = request.form.get("end_date")
    data = query_energy_data(start, end)
    return render_template("table.html", data=data, start=start, end=end)

@app.route("/analytics", methods=["GET", "POST"])
def analytics_view():
    start = end = None
    data = []
    if request.method == "POST":
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        data = query_energy_data(start, end)
        # Hvis brugeren vil downloade CSV
        if "download_csv" in request.form:
            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(["Date", "Hour", "SpotPriceDKK"])
            for r in data:
                cw.writerow([r["Date"], r["Hour"], r["SpotPriceDKK"]])
            mem = io.BytesIO()
            mem.write(si.getvalue().encode('utf-8'))
            mem.seek(0)
            si.close()
            filename = f"energy_data_{start}_to_{end}.csv"
            return send_file(mem, as_attachment=True, download_name=filename, mimetype="text/csv")

    return render_template("analytics.html", data=data, start=start, end=end)

if __name__ == "__main__":
    app.run(debug=True)
