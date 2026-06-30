from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionRequest, PredictionResponse
from app.ml_model import predict_fake_news
from app.explanation_service import generate_explanation
from app.semantic_search import semantic_search_service

app = FastAPI(
    title="Fake News Detector API",
    description="Backend API for the AI Fake News Detection Chrome Extension",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # okay for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "running", "message": "Fake News Detector API is live"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    model_result = predict_fake_news(request.text)
    similar_articles = semantic_search_service.find_similar(request.text)

    explanation = generate_explanation(
        label=model_result["label"],
        confidence=model_result["confidence"],
        risk_level=model_result["risk_level"],
        influential_words=model_result["influential_words"],
    )

    return PredictionResponse(
        label=model_result["label"],
        confidence=model_result["confidence"],
        risk_level=model_result["risk_level"],
        model_name=model_result["model_name"],
        influential_words=model_result["influential_words"],
        similar_articles=similar_articles,
        explanation=explanation,
    )