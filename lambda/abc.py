# import requests
# import os
# import time

# # --- Configuration ---
# OPENROUTER_API_KEY = "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"  # <-- replace with your valid key
# OPENROUTER_MODEL = "mistralai/mistral-nemo:free"  # working free model
# # ----------------------

# def summarize_article(url: str) -> str:
#     """Fetch article text and summarize using OpenRouter."""
#     try:
#         print("\nFetching article...")
#         html = requests.get(url, timeout=20).text
#     except Exception as e:
#         return f"Failed to fetch article: {str(e)}"

#     cleaned = " ".join(html.split())
#     text = cleaned[:2500]  # limit input size

#     if len(text) < 100:
#         return "The article content is too short or blocked for summarization."

#     api_url = "https://openrouter.ai/api/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://local-test",
#         "X-Title": "Local News Summarizer"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a precise and concise news summarizer. "
#                     "Summarize the article in 5–7 lines, highlighting key points clearly."
#                 )
#             },
#             {"role": "user", "content": text}
#         ]
#     }

#     for attempt in range(2):
#         try:
#             print("Contacting OpenRouter API...")
#             resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
#             if resp.status_code == 429:
#                 print("Rate limit hit, retrying...")
#                 time.sleep(1)
#                 continue
#             resp.raise_for_status()
#             data = resp.json()
#             summary = (
#                 data.get("choices", [{}])[0]
#                     .get("message", {})
#                     .get("content", "")
#                     .strip()
#             )
#             if not summary:
#                 return "No summary text returned by model."
#             return f"\n📰 News Summary:\n{summary}"
#         except Exception as e:
#             if attempt == 1:
#                 return f"Summarization failed: {str(e)}"
#     return "Unknown summarization error."

# # --- Main ---
# if __name__ == "__main__":
#     url = input("Enter the news article URL: ").strip()
#     if not url:
#         print("Please enter a valid URL.")
#     else:
#         result = summarize_article(url)
#         print(result)


import json
import os
from lambda_function import lambda_handler

# --- SET YOUR API KEY LOCALLY ---
os.environ["OPENROUTER_API_KEY"] = "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"  # replace with your working key

# --- Load simulated API Gateway event ---
with open("test_event.json", "r") as f:
    event = json.load(f)

# --- Invoke Lambda locally ---
result = lambda_handler(event, None)

print("\n=== Lambda Output ===")
print(json.dumps(result, indent=2))

