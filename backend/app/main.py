import math
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.explanation_service import generate_explanation
from app.ml_model import predict_fake_news
from app.models import AnalysisHistory
from app.schemas import (
    AdminHistoryResponse,
    AdminStatsResponse,
    HistoryItem,
    PredictionRequest,
    PredictionResponse,
)
from app.semantic_search import semantic_search_service


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
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
):
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


@app.get("/admin/stats", response_model=AdminStatsResponse)
def get_admin_stats(db: Session = Depends(get_db)):
    total_predictions = db.query(func.count(AnalysisHistory.id)).scalar() or 0

    fake_predictions = (
        db.query(func.count(AnalysisHistory.id))
        .filter(func.lower(AnalysisHistory.label) == "fake")
        .scalar()
        or 0
    )

    real_predictions = (
        db.query(func.count(AnalysisHistory.id))
        .filter(func.lower(AnalysisHistory.label) == "real")
        .scalar()
        or 0
    )

    start_of_today = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    predictions_today = (
        db.query(func.count(AnalysisHistory.id))
        .filter(AnalysisHistory.created_at >= start_of_today)
        .scalar()
        or 0
    )

    low_confidence_predictions = (
        db.query(func.count(AnalysisHistory.id))
        .filter(AnalysisHistory.confidence < 0.70)
        .scalar()
        or 0
    )

    average_confidence = (
        db.query(func.avg(AnalysisHistory.confidence)).scalar() or 0
    )

    return AdminStatsResponse(
        total_predictions=total_predictions,
        fake_predictions=fake_predictions,
        real_predictions=real_predictions,
        predictions_today=predictions_today,
        low_confidence_predictions=low_confidence_predictions,
        average_confidence=round(float(average_confidence), 4),
    )


@app.get("/admin/history", response_model=AdminHistoryResponse)
def get_admin_history(
    search: str | None = Query(default=None),
    label: str | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    min_confidence: float | None = Query(
        default=None,
        ge=0,
        le=1,
    ),
    max_confidence: float | None = Query(
        default=None,
        ge=0,
        le=1,
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(AnalysisHistory)

    if search:
        search_value = f"%{search.strip()}%"

        query = query.filter(
            or_(
                AnalysisHistory.input_text.ilike(search_value),
                AnalysisHistory.title.ilike(search_value),
                AnalysisHistory.url.ilike(search_value),
            )
        )

    if label:
        query = query.filter(
            func.lower(AnalysisHistory.label) == label.lower()
        )

    if risk_level:
        query = query.filter(
            func.lower(AnalysisHistory.risk_level) == risk_level.lower()
        )

    if min_confidence is not None:
        query = query.filter(
            AnalysisHistory.confidence >= min_confidence
        )

    if max_confidence is not None:
        query = query.filter(
            AnalysisHistory.confidence <= max_confidence
        )

    total = query.count()
    total_pages = math.ceil(total / page_size) if total else 0

    items = (
        query.order_by(AnalysisHistory.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return AdminHistoryResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.delete("/admin/history/{history_id}")
def delete_history_item(
    history_id: int,
    db: Session = Depends(get_db),
):
    history_item = (
        db.query(AnalysisHistory)
        .filter(AnalysisHistory.id == history_id)
        .first()
    )

    if history_item is None:
        raise HTTPException(
            status_code=404,
            detail="History item not found",
        )

    db.delete(history_item)
    db.commit()

    return {
        "message": "History item deleted",
        "id": history_id,
    }