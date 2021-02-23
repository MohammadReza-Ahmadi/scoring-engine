from datetime import date

from pydantic import BaseModel


class UndoneTrade(BaseModel):
    user_id: int = None
    calculation_start_date: date = None

    undue_trades_count: int = None
    past_due_trades_count: int = None
    arrear_trades_count: int = None

    undue_trades_total_balance_of_last_year: float = None
    past_due_trades_total_balance_of_last_year: float = None
    arrear_trades_total_balance_of_last_year: float = None
