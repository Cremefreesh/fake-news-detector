from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas import PredictionRequest, PredictionResponse, HistoryItem
from app.ml_model import predict_fake_news
from app.explanation_service import generate_explanation
from app.semantic_search import semantic_search_service
from app.database import Base, engine, get_db
from app.models import AnalysisHistory


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Fake News Detector API",
    description="Backend API for the AI Fake News Detection Chrome Extension",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Fake News Detector API is live",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    model_result = predict_fake_news(request.text)

    similar_articles = semantic_search_service.find_similar(request.text)

    explanation = generate_explanation(
        label=model_result["label"],
        confidence=model_result["confidence"],
        risk_level=model_result["risk_level"],
        influential_words=model_result["influential_words"],
        similar_articles=similar_articles,
    )

    history_item = AnalysisHistory(
        url=request.url,
        title=request.title,
        input_text=request.text,
        label=model_result["label"],
        confidence=model_result["confidence"],
        risk_level=model_result["risk_level"],
        model_name=model_result["model_name"],
        explanation=explanation,
    )

    db.add(history_item)
    db.commit()

    return PredictionResponse(
        label=model_result["label"],
        confidence=model_result["confidence"],
        risk_level=model_result["risk_level"],
        model_name=model_result["model_name"],
        influential_words=model_result["influential_words"],
        similar_articles=similar_articles,
        explanation=explanation,
    )


@app.get("/history", response_model=list[HistoryItem])
def get_history(db: Session = Depends(get_db)):
    return (
        db.query(AnalysisHistory)
        .order_by(AnalysisHistory.created_at.desc())
        .limit(20)
        .all()
    )