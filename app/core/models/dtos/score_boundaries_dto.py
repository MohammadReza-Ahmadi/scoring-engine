from pydantic import BaseModel


class ScoreBoundariesDTO(BaseModel):
    min_score: int = 0
    max_score: int = 0
    identities_max_score: int = 0
    histories_max_score: int = 0
    volumes_max_score: int = 0
    timeliness_max_score: int = 0
