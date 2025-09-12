from flask import Blueprint, render_template, request
import sqlite3
import pandas as pd
from collections import defaultdict
import datetime

analytics = Blueprint('analytics', __name__)
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

def aggregate_daily(data):
    agg = defaultdict(list)
    for r in data: agg[r["Hour"]].append(r["SpotPriceDKK"])
    return [{"Hour": h, "AvgPrice": sum(v)/len(v)} for h,v in sorted(agg.items())]

def aggregate_weekday(data):
    agg = defaultdict(list)
    for r in data:
        dt = datetime.datetime.strptime(r["Date"], "%Y-%m-%d")
        agg[dt.weekday()].append(r["SpotPriceDKK"])
    return [{"Weekday": k, "AvgPrice": sum(v)/len(v)} for k,v in sorted(agg.items())]

def aggregate_hour_weekday(data):
    temp = defaultdict(list)
    for r in data:
        dt = datetime.datetime.strptime(r["Date"], "%Y-%m-%d")
        h = int(r["Hour"].split(":")[0])
        temp[(h, dt.weekday())].append(r["SpotPriceDKK"])
    result=[]
    for (h, wd), v in temp.items(): result.append({"Hour":h,"Weekday":wd,"AvgPrice":sum(v)/len(v)})
    return result

def compute_metrics(data):
    """Lav nøglemetrics til farvede kort"""
    if not data:
        return {}
    prices = [r["SpotPriceDKK"] for r in data]
    avg_price = sum(prices)/len(prices)
    max_price = max(prices)
    min_price = min(prices)
    return {
        "average": round(avg_price,2),
        "max": round(max_price,2),
        "min": round(min_price,2),
        "prices": prices[-24:]  # sidste 24 timer til mini-graf
    }

@analytics.route("/analytics", methods=["GET"])
def analytics_view():
    tab = request.args.get("tab", "overview")
    chart_type = request.args.get("chart_type", "line")
    start = request.args.get("start_date")
    end = request.args.get("end_date")
    data = []
    metrics = {}

    if start and end:
        raw = query_energy_data(start, end)
        metrics = compute_metrics(raw)
        if tab=="overview":
            data = raw
            if chart_type=="moving_avg":
                df = pd.DataFrame(raw)
                df['Datetime'] = pd.to_datetime(df['Date']+" "+df['Hour'])
                df.sort_values('Datetime', inplace=True)
                df['MA7'] = df['SpotPriceDKK'].rolling(7).mean()
                data = df.to_dict(orient='records')
        elif tab=="daily":
            data = aggregate_daily(raw)
        elif tab=="weekday":
            data = aggregate_weekday(raw)
        elif tab=="hour_weekday":
            data = aggregate_hour_weekday(raw)

    return render_template(
        "analytics.html",
        data=data,
        metrics=metrics,
        tab=tab,
        chart_type=chart_type,
        start=start,
        end=end
    )
