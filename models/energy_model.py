class EnergyRecord:
    """Model for en enkelt energipris-række."""
    def __init__(self, hour_utc: str, date: str, hour: str, price_dkk: float):
        self.hour_utc = hour_utc
        self.date = date
        self.hour = hour
        self.price = price_dkk

    def to_dict(self):
        return {
            "HourUTC": self.hour_utc,
            "Date": self.date,
            "Hour": self.hour,
            "SpotPriceDKK": self.price
        }
