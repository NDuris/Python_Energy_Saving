from datetime import datetime, timedelta
from db_manager import insert_data
from data_fetcher import fetch_energy_prices
from data_cleaner import clean_energy_data

if __name__ == "__main__":
    end = datetime.utcnow().date()
    start = end - timedelta(days=1)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    print(f"Henter data fra {start_str} til {end_str} ...")
    raw = fetch_energy_prices(area="DK1", start=start_str, end=end_str)
    cleaned = clean_energy_data(raw)
    insert_data(cleaned)
    print(f"Indsat {len(cleaned)} nye rækker i databasen ✅")
