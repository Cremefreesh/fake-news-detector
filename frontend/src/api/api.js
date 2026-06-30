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
    throw new Error("Failed to analyse text");
  }

  return response.json();
}

export async function getCurrentPageText() {
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true,
  });

  const [result] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const article = document.querySelector("article");
      const title = document.title || "";

      const text = article
        ? article.innerText
        : document.body.innerText;

      return `${title}\n\n${text}`;
    },
  });

  return result.result;
}