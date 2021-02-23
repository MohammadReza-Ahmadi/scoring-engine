class DateDiff:
    days: int
    months: int
    years: int

    def __init__(self, days: int = 0, months: int = 0, years: int = 0) -> None:
        self.days = days
        self.months = months
        self.years = years
