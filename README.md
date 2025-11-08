#  Serverless News Summarizer — AWS Lambda (Python) + OpenRouter + Terraform + HTML Frontend

This project is a **Serverless News Summarizer** built using **AWS Lambda**, **API Gateway**, and **OpenRouter’s Mistral model**.  
It takes a news article URL or raw text as input and returns a clean 5–7 line summary — all powered by serverless infrastructure with no database required.

---
##  Live Demo

**Frontend (Deployed on Netlify):**  
 [https://heartfelt-starship-b20b18.netlify.app](https://heartfelt-starship-b20b18.netlify.app)

Try it live — paste any news article link or text and get an instant summary powered by AWS Lambda + OpenRouter.

## Tech Stack

- **Backend:** Python (AWS Lambda + API Gateway)
- **Frontend:** HTML, CSS, JavaScript
- **AI Model:** OpenRouter API (`mistralai/mistral-nemo:free`)
- **Infrastructure:** Terraform (for automated deployment)
- **Hosting Region:** AWS `ap-south-1` (Mumbai)

---

##  Project Overview

The system has two main parts:

1. **Serverless Backend (Lambda + API Gateway)**  
   - Receives POST requests with a news article URL or text.  
   - Extracts and cleans article content.  
   - Sends the text to the **OpenRouter API** for summarization.  
   - Returns a short, human-readable summary.

2. **Frontend (HTML + CSS + JS)**  
   - Simple, fast, and responsive web interface.  
   - Lets users paste a URL or type text.  
   - Displays the summary instantly without reloading.  

---

##  Folder Structure

serverless-news-summarizer/
├── lambda/ # Python backend logic
│ ├── lambda_function.py
│ └── requirements.txt
│
├── terraform/ # Infrastructure-as-code setup
│ ├── main.tf
│ ├── provider.tf
│ ├── variables.tf
│ ├── outputs.tf
│ └── terraform.tfstate
│
├── frontend/ # Static web interface
│ ├── index.html
│ ├── style.css
│ ├── script.js
│ └── README.md
│
└── README.md

## Deploy the Backend (AWS Lambda + Terraform)

1. Navigate to your Lambda code folder:
   ```bash
   cd lambda
   pip install -r requirements.txt -t .
   zip -r lambda.zip .
   
2.Deploy with Terraform:

cd ../terraform
terraform init
terraform apply -var "openrouter_key=YOUR_OPENROUTER_API_KEY" -var "aws_region=ap-south-1"

3.Copy the post_summarize_url value from Terraform output
Example:
post_summarize_url = "https://vrgb71ndoh.execute-api.ap-south-1.amazonaws.com/summarize"

### Run the Frontend (HTML + JS)

1.Open the frontend/script.js file and update the line:

const API_URL = "https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/summarize";


2.Run a local server:

cd frontend
python -m http.server 8080


3.Visit: http://localhost:8080

4.Paste any article URL or text, and click Summarize 🪄

### Test with Curl (optional)

You can also test your Lambda endpoint directly:

curl -X POST "https://vrgb71ndoh.execute-api.ap-south-1.amazonaws.com/summarize" \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.bbc.com/news"}'
## How It Works

User input (URL or text) → sent via POST request.

Lambda fetches the article, cleans HTML content.

Trims the text to prevent API overload.

Sends the text to OpenRouter’s Mistral model.

Returns a clean, 5–7 line summary.

## Notes

This version uses OpenRouter instead of Hugging Face.

No database or external storage is used — it’s 100% stateless.

The whole setup runs within the AWS Free Tier.

Can be extended to use newspaper3k or BeautifulSoup for better text extraction.

## Future Enhancements

Add text upload support (e.g., .txt or .pdf)

Enable summary length selection (short / detailed)

Add voice summary output using AWS Polly

Deploy frontend on AWS S3 or Netlify
