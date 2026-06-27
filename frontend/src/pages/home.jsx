import { useState } from "react";
import { predictFakeNews } from "../api/api";
import Button from "../components/Button/Button";
import TextArea from "../components/TextArea/TextArea";
import LoadingSpinner from "../components/LoadingSpinner/LoadingSpinner";
import PredictionCard from "../components/PredictionCard/PredictionCard";

function Home() {
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
    } catch {
      setError("Could not connect to the prediction API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="home-page">
      <section className="hero">
        <p className="eyebrow">AI Browser Safety Tool</p>
        <h1>Fake News Detector</h1>
        <p className="subtitle">
          Paste a headline, article paragraph, or social media post and get an
          instant credibility prediction.
        </p>
      </section>

      <TextArea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste suspicious content here..."
      />

      <Button onClick={handleAnalyse} disabled={loading}>
        {loading ? "Analysing..." : "Analyse content"}
      </Button>

      {loading && <LoadingSpinner />}

      {error && <p className="error-message">{error}</p>}

      <PredictionCard result={result} />
    </main>
  );
}

export default Home;