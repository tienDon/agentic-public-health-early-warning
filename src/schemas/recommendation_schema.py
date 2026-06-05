# src/schemas/recommendation_schema.py

from pydantic import BaseModel
from typing import List


class RecommendationItem(BaseModel):
    priority: str
    action: str


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]