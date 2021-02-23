from pydantic import BaseModel


class ScoreDetailsDTO(BaseModel):
    score: int = 0
    identities_score: int = 0
    histories_score: int = 0
    volumes_score: int = 0
    timeliness_score: int = 0
