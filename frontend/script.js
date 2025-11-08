const API_URL = "https://vrgb71ndoh.execute-api.ap-south-1.amazonaws.com/summarize";

const summarizeBtn = document.getElementById("summarizeBtn");
const urlInput = document.getElementById("urlInput");
const loader = document.getElementById("loader");
const summaryBox = document.getElementById("summaryBox");
const summaryText = document.getElementById("summaryText");
const themeToggle = document.getElementById("themeToggle");
const body = document.body;

summarizeBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();
  if (!url) {
    alert("Please enter a valid news article URL.");
    return;
  }

  loader.style.display = "block";
  summaryBox.style.display = "none";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    loader.style.display = "none";

    if (response.ok && data.summary) {
      summaryText.textContent = data.summary;
      summaryBox.style.display = "block";
    } else {
      alert(data.error || "Failed to summarize. Please try again.");
    }
  } catch (error) {
    loader.style.display = "none";
    alert("Network error: " + error.message);
  }
});

function copySummary() {
  const text = summaryText.textContent;
  navigator.clipboard.writeText(text).then(() => {
    alert("Summary copied to clipboard!");
  });
}

// Theme Toggle
themeToggle.addEventListener("click", () => {
  const isLight = body.classList.contains("light-mode");
  body.classList.toggle("light-mode", !isLight);
  body.classList.toggle("dark-mode", isLight);
  themeToggle.textContent = isLight ? " Light Mode" : " Dark Mode";
});
