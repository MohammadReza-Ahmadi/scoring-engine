from datetime import date

from pydantic import BaseModel


class ScoreChangesDTO(BaseModel):
    title: str = None
    change_date: date = None
    score_change: int = None
