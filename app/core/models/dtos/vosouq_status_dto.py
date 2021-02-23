from pydantic import BaseModel


class VosouqStatusDTO(BaseModel):
    membership_duration_day: int = 0
    membership_duration_month: int = 0
    done_trades_count: int = 0
    undone_trades_count: int = 0
    negative_status_count: int = 0
    delay_days_count_avg: int = 0
    recommend_to_others_count: int = 0
