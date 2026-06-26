from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionRequest, PredictionResponse
from app.ml_model import predict_fake_news
from app.explanation_service import generate_explanation


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

    explanation = generate_explanation(
        text=request.text,
        label=model_result["label"],
        confidence=model_result["confidence"],
    )

    return PredictionResponse(
        label=model_result["label"],
        confidence=model_result["confidence"],
        explanation=explanation,
    )