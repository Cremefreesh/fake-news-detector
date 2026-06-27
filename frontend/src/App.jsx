import { useState } from "react";
import { predictFakeNews } from "./services/api";
import PredictionCard from "./components/PredictionCard/PredictionCard";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyse() {
    if (!text.trim()) {
      setError("Please enter some text to analyse.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const prediction = await predictFakeNews(text);
      setResult(prediction);
    } catch (err) {
      setError("Something went wrong while analysing the text.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <h1>AI Fake News Detector</h1>

      <p className="subtitle">
        Paste a news headline, article paragraph, or social media post to analyse it.
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste suspicious content here..."
      />

      <button onClick={handleAnalyse} disabled={loading}>
        {loading ? "Analysing..." : "Analyse"}
      </button>

      {error && <p className="error">{error}</p>}

      <PredictionCard result={result} />
    </main>
  );
}

export default App;