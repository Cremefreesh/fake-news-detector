import { useState } from "react";
import { predictFakeNews, getCurrentPageText, getHistory } from "../api/api";
import Button from "../components/Button/Button";
import TextArea from "../components/TextArea/TextArea";
import LoadingSpinner from "../components/LoadingSpinner/LoadingSpinner";
import PredictionCard from "../components/PredictionCard/PredictionCard";
import HistoryList from "../components/HistoryList/HistoryList";

function Home() {
  const [activeTab, setActiveTab] = useState("analyse");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
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

  async function handleLoadHistory() {
    try {
      setActiveTab("history");
      setLoading(true);
      setError("");

      const historyData = await getHistory();
      setHistory(historyData);
    } catch {
      setError("Could not load analysis history.");
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
          Analyse article credibility and review previous scans.
        </p>
      </section>

      <div className="tab-row">
        <button
          className={activeTab === "analyse" ? "tab-button active" : "tab-button"}
          onClick={() => setActiveTab("analyse")}
        >
          Analyse
        </button>

        <button
          className={activeTab === "history" ? "tab-button active" : "tab-button"}
          onClick={handleLoadHistory}
        >
          History
        </button>
      </div>

      {activeTab === "analyse" && (
        <>
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

          <PredictionCard result={result} />
        </>
      )}

      {activeTab === "history" && <HistoryList history={history} />}

      {loading && <LoadingSpinner />}

      {error && <p className="error-message">{error}</p>}
    </main>
  );
}

export default Home;