import "./HistoryList.css";

function HistoryList({ history }) {
  if (!history.length) {
    return (
      <section className="history-empty">
        <p>No analyses saved yet.</p>
      </section>
    );
  }

  return (
    <section className="history-list">
      {history.map((item) => (
        <article key={item.id} className="history-item">
          <div className="history-item-header">
            <p className="history-title">
              {item.title || item.url || "Untitled analysis"}
            </p>

            <span className={`history-badge ${item.label.replaceAll(" ", "-").toLowerCase()}`}>
              {item.label}
            </span>
          </div>

          <p className="history-meta">
            {Math.round(item.confidence * 100)}% confidence · {item.risk_level} risk
          </p>

          <p className="history-explanation">{item.explanation}</p>

          <p className="history-date">
            {new Date(item.created_at).toLocaleString()}
          </p>
        </article>
      ))}
    </section>
  );
}

export default HistoryList;