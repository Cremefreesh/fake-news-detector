function PredictionCard({ result }) {
  if (!result) return null;

  return (
    <div className="prediction-card">
      <h2>{result.label}</h2>

      <p>
        <strong>Confidence:</strong> {Math.round(result.confidence * 100)}%
      </p>

      <p>
        <strong>Explanation:</strong> {result.explanation}
      </p>
    </div>
  );
}

export default PredictionCard;