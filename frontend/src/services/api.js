const API_BASE_URL = "http://127.0.0.1:8000";

export async function predictFakeNews(text) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error("Prediction request failed");
  }

  return response.json();
}