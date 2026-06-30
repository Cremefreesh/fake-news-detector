import { useState } from "react";
import { predictFakeNews, getCurrentPageText } from "../api/api";
import Button from "../components/Button/Button";
import TextArea from "../components/TextArea/TextArea";
import LoadingSpinner from "../components/LoadingSpinner/LoadingSpinner";
import PredictionCard from "../components/PredictionCard/PredictionCard";

function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function analyseText(textToAnalyse) {
    if (!textToAnalyse.trim()) {
      setError("Please enter or scan some text to analyse.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const prediction = await predictFakeNews(textToAnalyse);
      setResult(prediction);
    } catch {
      setError("Could not connect to the prediction API.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAnalyse() {
    await analyseText(text);
  }

  async function handleScanPage() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const pageText = await getCurrentPageText();
      setText(pageText.slice(0, 3000));

      await analyseText(pageText);
    } catch {
      setError("Could not scan the current page. Try refreshing the page.");
      setLoading(false);
    }
  }

  return (
    <main className="home-page">
      <section className="hero">
        <p className="eyebrow">AI Browser Safety Tool</p>
        <h1>Fake News Detector</h1>
        <p className="subtitle">
          Paste text or scan the current webpage for a credibility prediction.
        </p>
      </section>

      <TextArea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste suspicious content here..."
      />

      <Button onClick={handleAnalyse} disabled={loading}>
        {loading ? "Analysing..." : "Analyse pasted text"}
      </Button>

      <Button onClick={handleScanPage} disabled={loading}>
        Scan current page
      </Button>

      {loading && <LoadingSpinner />}

      {error && <p className="error-message">{error}</p>}

      <PredictionCard result={result} />
    </main>
  );
}

export default Home;