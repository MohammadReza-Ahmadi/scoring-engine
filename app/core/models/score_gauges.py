from pydantic import BaseModel, Field


class ScoreGauge(BaseModel):
    start: int = Field(None)
    end: int = Field(None)
    title: str = Field(None)
    color: str = Field(None)
    risk_status: str = Field(None)

    # class Config:
    # orm_mode = True
    # exclude_fields = ['COLLECTION_NAME']
