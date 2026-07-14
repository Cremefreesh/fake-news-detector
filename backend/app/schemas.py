from datetime import datetime

from pydantic import BaseModel, Field


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
    input_text: str
    label: str
    confidence: float
    risk_level: str
    model_name: str
    explanation: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminStatsResponse(BaseModel):
    total_predictions: int
    fake_predictions: int
    real_predictions: int
    predictions_today: int
    low_confidence_predictions: int
    average_confidence: float


class AdminHistoryResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    page: int
    page_size: int
    total_pages: int