from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    label: str
    confidence: float
    risk_level: str
    model_name: str
    influential_words: list[str]
    similar_articles: list[SimilarArticle]
    explanation: str

    
class SimilarArticle(BaseModel):
    label: str
    similarity: float
    preview: str