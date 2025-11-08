# Serverless News Summarizer — React + AWS Lambda (Python) + Terraform (Hugging Face, No DB)

## 1) Backend deploy (Lambda + API Gateway via Terraform)
```bash
cd lambda
pip install -r requirements.txt -t .
zip -r lambda.zip .
cd ../terraform
terraform init
terraform apply -var "hf_token=YOUR_HF_API_TOKEN" -var "aws_region=ap-south-1"
# copy the `post_summarize_url` from outputs
```

## 2) Frontend run (React)
```bash
cd ../frontend
cp .env.example .env   # put the post_summarize_url into REACT_APP_API_URL
npm install
npm start
```

## 3) Test with curl
```bash
curl -X POST "$(terraform -chdir=terraform output -raw post_summarize_url)"       -H "Content-Type: application/json"       -d '{"url":"https://www.bbc.com/news"}'
```

## Notes
- Simple mode: Lambda fetches raw HTML, truncates, and sends to Hugging Face model (default: facebook/bart-large-cnn).
- For better quality, switch to an article-text extraction approach (e.g., newspaper3k), but that increases package size.
