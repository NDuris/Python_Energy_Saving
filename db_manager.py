import sqlite3
from pathlib import Path
from typing import List
from models.energy_model import EnergyRecord

DB_PATH = Path("energy_data.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS energy (
                HourUTC TEXT PRIMARY KEY,
                Date TEXT,
                Hour TEXT,
                SpotPriceDKK REAL
            )
        """)
        conn.commit()

def insert_data(records: List[EnergyRecord]):
    rows = [r.to_dict() for r in records]
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.executemany("""
            INSERT OR IGNORE INTO energy (HourUTC, Date, Hour, SpotPriceDKK)
            VALUES (:HourUTC, :Date, :Hour, :SpotPriceDKK)
        """, rows)
        conn.commit()
        print(f"Faktisk tilføjede rækker: {c.rowcount}")

