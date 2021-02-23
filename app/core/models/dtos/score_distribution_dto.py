from pydantic import BaseModel


class ScoreDistributionDTO(BaseModel):
    from_score: int = 0
    to_score: int = 0
    count: int = 0
