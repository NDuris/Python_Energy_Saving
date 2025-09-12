from flask import Blueprint, render_template, request
import sqlite3

main_bp = Blueprint("main", __name__)
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

@main_bp.route("/", methods=["GET", "POST"])
def table_view():
    start = end = None
    if request.method == "POST":
        start = request.form.get("start_date")
        end = request.form.get("end_date")
    data = query_energy_data(start, end)
    return render_template("table.html", data=data, start=start, end=end)
