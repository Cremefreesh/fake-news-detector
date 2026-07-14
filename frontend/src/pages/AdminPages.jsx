import { useCallback, useEffect, useState } from "react";

import {
  deleteAdminHistoryItem,
  getAdminHistory,
  getAdminStats,
} from "../api/api";

import "../styles/admin.css";


const EMPTY_STATS = {
  total_predictions: 0,
  fake_predictions: 0,
  real_predictions: 0,
  predictions_today: 0,
  low_confidence_predictions: 0,
  average_confidence: 0,
};


function formatConfidence(confidence) {
  return `${(confidence * 100).toFixed(1)}%`;
}


function formatDate(dateValue) {
  return new Date(dateValue).toLocaleString();
}


function shortenText(text, maximumLength = 150) {
  if (!text) {
    return "No text available";
  }

  if (text.length <= maximumLength) {
    return text;
  }

  return `${text.slice(0, maximumLength)}...`;
}


function AdminPage() {
  const [stats, setStats] = useState(EMPTY_STATS);
  const [history, setHistory] = useState([]);
  const [searchInput, setSearchInput] = useState("");
  const [activeSearch, setActiveSearch] = useState("");
  const [label, setLabel] = useState("");
  const [riskLevel, setRiskLevel] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(0);
  const [totalResults, setTotalResults] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  const loadStats = useCallback(async () => {
    const statsData = await getAdminStats();
    setStats(statsData);
  }, []);


  const loadHistory = useCallback(async () => {
    const historyData = await getAdminHistory({
      search: activeSearch,
      label,
      riskLevel,
      page,
      pageSize,
    });

    setHistory(historyData.items);
    setTotalPages(historyData.total_pages);
    setTotalResults(historyData.total);
  }, [
    activeSearch,
    label,
    riskLevel,
    page,
    pageSize,
  ]);


  const loadDashboard = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadStats(),
        loadHistory(),
      ]);
    } catch (requestError) {
      console.error(requestError);

      setError(
        "Could not load the admin dashboard. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }, [loadHistory, loadStats]);


  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);


  function handleSearch(event) {
    event.preventDefault();

    setPage(1);
    setActiveSearch(searchInput);
  }


  function clearFilters() {
    setSearchInput("");
    setActiveSearch("");
    setLabel("");
    setRiskLevel("");
    setPage(1);
  }


  async function handleDelete(historyId) {
    const shouldDelete = window.confirm(
      "Are you sure you want to delete this prediction?"
    );

    if (!shouldDelete) {
      return;
    }

    try {
      setError("");

      await deleteAdminHistoryItem(historyId);

      await Promise.all([
        loadStats(),
        loadHistory(),
      ]);
    } catch (requestError) {
      console.error(requestError);
      setError("Could not delete the prediction.");
    }
  }


  return (
    <main className="admin-page">
      <section className="admin-header">
        <div>
          <p className="admin-eyebrow">
            Model monitoring
          </p>

          <h1>Admin dashboard</h1>

          <p className="admin-description">
            Review predictions, inspect confidence scores and monitor how the
            fake-news model is being used.
          </p>
        </div>

        <button
          className="admin-refresh-button"
          type="button"
          onClick={loadDashboard}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "Refresh data"}
        </button>
      </section>


      {error && (
        <div className="admin-error">
          {error}
        </div>
      )}


      <section className="admin-stats-grid">
        <article className="admin-stat-card">
          <span>Total predictions</span>
          <strong>{stats.total_predictions}</strong>
        </article>

        <article className="admin-stat-card">
          <span>Fake predictions</span>
          <strong>{stats.fake_predictions}</strong>
        </article>

        <article className="admin-stat-card">
          <span>Real predictions</span>
          <strong>{stats.real_predictions}</strong>
        </article>

        <article className="admin-stat-card">
          <span>Predictions today</span>
          <strong>{stats.predictions_today}</strong>
        </article>

        <article className="admin-stat-card">
          <span>Average confidence</span>
          <strong>
            {formatConfidence(stats.average_confidence)}
          </strong>
        </article>

        <article className="admin-stat-card">
          <span>Below 70% confidence</span>
          <strong>{stats.low_confidence_predictions}</strong>
        </article>
      </section>


      <section className="admin-table-section">
        <div className="admin-table-heading">
          <div>
            <h2>Prediction history</h2>
            <p>
              {totalResults} matching prediction
              {totalResults === 1 ? "" : "s"}
            </p>
          </div>
        </div>


        <form
          className="admin-filters"
          onSubmit={handleSearch}
        >
          <input
            type="search"
            placeholder="Search article text, title or URL"
            value={searchInput}
            onChange={(event) => {
              setSearchInput(event.target.value);
            }}
          />

          <select
            value={label}
            onChange={(event) => {
              setPage(1);
              setLabel(event.target.value);
            }}
          >
            <option value="">All labels</option>
            <option value="fake">Fake</option>
            <option value="real">Real</option>
          </select>

          <select
            value={riskLevel}
            onChange={(event) => {
              setPage(1);
              setRiskLevel(event.target.value);
            }}
          >
            <option value="">All risk levels</option>
            <option value="high">High risk</option>
            <option value="medium">Medium risk</option>
            <option value="low">Low risk</option>
          </select>

          <button type="submit">
            Search
          </button>

          <button
            className="admin-secondary-button"
            type="button"
            onClick={clearFilters}
          >
            Clear
          </button>
        </form>


        {loading ? (
          <div className="admin-table-message">
            Loading prediction history...
          </div>
        ) : history.length === 0 ? (
          <div className="admin-table-message">
            No predictions match the selected filters.
          </div>
        ) : (
          <div className="admin-table-wrapper">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Article</th>
                  <th>Prediction</th>
                  <th>Confidence</th>
                  <th>Risk</th>
                  <th>Model</th>
                  <th>Created</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td className="admin-article-cell">
                      <strong>
                        {item.title || "Untitled analysis"}
                      </strong>

                      <p>
                        {shortenText(item.input_text)}
                      </p>

                      {item.url && (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          View source
                        </a>
                      )}
                    </td>

                    <td>
                      <span
                        className={`admin-badge admin-badge-${item.label.toLowerCase()}`}
                      >
                        {item.label}
                      </span>
                    </td>

                    <td>
                      {formatConfidence(item.confidence)}
                    </td>

                    <td>
                      <span
                        className={`admin-risk admin-risk-${item.risk_level.toLowerCase()}`}
                      >
                        {item.risk_level}
                      </span>
                    </td>

                    <td>{item.model_name}</td>

                    <td>
                      {formatDate(item.created_at)}
                    </td>

                    <td>
                      <button
                        className="admin-delete-button"
                        type="button"
                        onClick={() => {
                          handleDelete(item.id);
                        }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}


        <div className="admin-pagination">
          <button
            type="button"
            disabled={page <= 1 || loading}
            onClick={() => {
              setPage((currentPage) => currentPage - 1);
            }}
          >
            Previous
          </button>

          <span>
            Page {page} of {totalPages || 1}
          </span>

          <button
            type="button"
            disabled={
              page >= totalPages ||
              totalPages === 0 ||
              loading
            }
            onClick={() => {
              setPage((currentPage) => currentPage + 1);
            }}
          >
            Next
          </button>
        </div>
      </section>
    </main>
  );
}


export default AdminPage;