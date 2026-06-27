import "./PredictionCard.css";

function PredictionCard({ result }) {
  if (!result) return null;

  return (
    <section className="prediction-card">
      <p className="result-label">{result.label}</p>
      <p className="confidence">
        Confidence: {Math.round(result.confidence * 100)}%
      </p>
      <p className="explanation">{result.explanation}</p>
    </section>
  );
}

export default PredictionCard;