from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from app.database import Base


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    input_text = Column(Text, nullable=False)

    label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)