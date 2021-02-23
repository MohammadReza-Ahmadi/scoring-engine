from datetime import date

from pydantic import BaseModel


class DoneTrade(BaseModel):
    user_id: int = None
    calculation_start_date: date = None

    timely_trades_count_of_last_3_months: int = None
    past_due_trades_count_of_last_3_months: int = None
    arrear_trades_count_of_last_3_months: int = None

    timely_trades_count_between_last_3_to_12_months: int = None
    past_due_trades_count_between_last_3_to_12_months: int = None
    arrear_trades_count_between_last_3_to_12_months: int = None

    trades_total_balance: float = None
    total_delay_days: int = None
