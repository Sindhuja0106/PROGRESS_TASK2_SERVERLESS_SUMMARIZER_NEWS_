import json
import os
import requests
import time

# --- Configuration ---
OPENROUTER_MODEL = "mistralai/mistral-nemo:free"
# ----------------------

def _response(status, payload):
    """Helper to return standard API Gateway JSON response with CORS headers."""
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps(payload),
    }

def lambda_handler(event, context):
    """AWS Lambda handler"""
    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return _response(200, {"ok": True})

    # Parse incoming request body
    try:
        body_raw = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            import base64
            body_raw = base64.b64decode(body_raw).decode("utf-8")
        body = json.loads(body_raw)
    except Exception:
        return _response(400, {"error": "Invalid JSON body"})

    url = (body or {}).get("url")
    if not url:
        return _response(400, {"error": "'url' is required in JSON body"})

    try:
        summary = summarize_article(url)
        return _response(200, {"summary": summary})
    except Exception as e:
        return _response(500, {"error": str(e)})


def summarize_article(url: str) -> str:
    """Fetch article text and summarize using OpenRouter."""
    try:
        print("Fetching article...")
        html = requests.get(url, timeout=20).text
    except Exception as e:
        return f"Failed to fetch article: {str(e)}"

    cleaned = " ".join(html.split())
    text = cleaned[:2500]

    if len(text) < 100:
        return "The article content is too short or blocked for summarization."

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Missing OPENROUTER_API_KEY environment variable."

    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://lambda.news-summarizer",
        "X-Title": "AWS Lambda Summarizer"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise and concise news summarizer. "
                    "Summarize the article in 5–7 lines, highlighting key points clearly."
                )
            },
            {"role": "user", "content": text}
        ]
    }

    for attempt in range(2):
        try:
            print("Contacting OpenRouter API...")
            resp = requests.post(api_url, headers=headers, json=payload, timeout=60)

            # Retry on rate limit
            if resp.status_code == 429:
                print("Rate limit hit, retrying...")
                time.sleep(1)
                continue

            resp.raise_for_status()
            data = resp.json()

            summary = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
            )

            if not summary:
                return "No summary text returned by model."

            return f"📰 News Summary:\n{summary}"

        except Exception as e:
            if attempt == 1:
                return f"Summarization failed: {str(e)}"

    return "Unknown summarization error."
