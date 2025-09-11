# daily_update.py
from datetime import datetime, timedelta, timezone
from db_manager import init_db, get_latest_hourutc, insert_data
from data_fetcher import fetch_energy_prices
from data_cleaner import clean_energy_data

if __name__ == "__main__":
    init_db()
    last = get_latest_hourutc()
    if last:
        # Parse last fra DB (husk Z-case)
        if last.endswith("Z"):
            last_iso = last.replace("Z", "+00:00")
        else:
            last_iso = last
        start = datetime.fromisoformat(last_iso).astimezone(timezone.utc) + timedelta(hours=1)
    else:
        # fallback: hent sidste døgn hvis DB er tom
        start = datetime.now(timezone.utc) - timedelta(days=1)

    end = datetime.now(timezone.utc)

    print(f"Henter data fra {start.isoformat()} til {end.isoformat()} ...")
    raw = fetch_energy_prices(start=start.isoformat(), end=end.isoformat())
    cleaned = clean_energy_data(raw)
    insert_data(cleaned)
    print(f"Tilføjede {len(cleaned)} nye rækker ✅")
