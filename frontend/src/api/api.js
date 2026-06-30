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
      function getMetaContent(name) {
        const tag =
          document.querySelector(`meta[name="${name}"]`) ||
          document.querySelector(`meta[property="${name}"]`);

        return tag ? tag.content : "";
      }

      const title =
        document.querySelector("h1")?.innerText ||
        document.title ||
        getMetaContent("og:title");

      const description =
        getMetaContent("description") ||
        getMetaContent("og:description");

      const article =
        document.querySelector("article") ||
        document.querySelector("main") ||
        document.body;

      const paragraphs = Array.from(article.querySelectorAll("p"))
        .map((p) => p.innerText.trim())
        .filter((text) => text.length > 40);

      const articleText = paragraphs.join("\n\n");

      return `${title}\n\n${description}\n\n${articleText}`.trim();
    },
  });

  return result.result;
}