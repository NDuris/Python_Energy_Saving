from models.energy_model import EnergyRecord

def clean_energy_data(raw_data):
    cleaned = []
    for row in raw_data:
        hour_dk = row.get("HourDK")
        price = row.get("SpotPriceDKK")
        if not hour_dk or price is None:
            continue

        # Splitter dato og timer
        if "T" in hour_dk:  # format 2025-08-14T02:00:00
            date, hour_full = hour_dk.split("T")
            hour = hour_full[:5]  # 'HH:MM' ?åbenbart
        else:
            date = hour_dk
            hour = "00:00"

        rec = EnergyRecord(
            hour_utc=row["HourUTC"],
            date=date,
            hour=hour,
            price_dkk=round(price, 2)
        )
        cleaned.append(rec)
    return cleaned
