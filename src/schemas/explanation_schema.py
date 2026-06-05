# src/schemas/explanation_schema.py

from pydantic import BaseModel

class ExplanationItem(BaseModel):
    rank: int       
    feature: str
    impact: float
    direction: str
    reason: str

class ExplanationResponse(BaseModel):
    summary: str