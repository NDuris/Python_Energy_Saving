from datetime import datetime, timedelta
from db_manager import init_db, insert_data
from data_fetcher import fetch_energy_prices
from data_cleaner import clean_energy_data

if __name__ == "__main__":
    init_db()

    end = datetime.utcnow().date()
    start = end - timedelta(days=365)  # 1 års data

    chunk_days = 30  # henter 1 måned ad gangen
    current = start
    total_inserted = 0

    while current < end:
        chunk_end = min(current + timedelta(days=chunk_days), end)

        start_str = current.strftime("%Y-%m-%d")
        end_str = chunk_end.strftime("%Y-%m-%d")

        print(f"Henter data fra {start_str} til {end_str} ...")
        raw = fetch_energy_prices(area="DK1", start=start_str, end=end_str)
        cleaned = clean_energy_data(raw)
        insert_data(cleaned)
        total_inserted += len(cleaned)
        print(f"Indsat {len(cleaned)} rækker ✅")

        current = chunk_end + timedelta(days=1)

    print(f"Færdig! Total rækker indsat: {total_inserted}")
