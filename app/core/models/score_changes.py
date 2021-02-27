from datetime import date

from pydantic import BaseModel


class ScoreChange(BaseModel):
    user_id: int = None
    reason_rule_code: str = None
    reason_desc: str = None
    change_date: date = None
    score_change: int = None
    score: int = None
