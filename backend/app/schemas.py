from pydantic import BaseModel, Field
from datetime import datetime


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1)
    url: str | None = None
    title: str | None = None


class SimilarArticle(BaseModel):
    label: str
    similarity: float
    preview: str


class PredictionResponse(BaseModel):
    label: str
    confidence: float
    risk_level: str
    model_name: str
    influential_words: list[str]
    similar_articles: list[SimilarArticle]
    explanation: str


class HistoryItem(BaseModel):
    id: int
    url: str | None
    title: str | None
    label: str
    confidence: float
    risk_level: str
    model_name: str
    explanation: str
    created_at: datetime

    class Config:
        from_attributes = True