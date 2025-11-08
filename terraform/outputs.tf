output "api_base_url" {
  value       = aws_apigatewayv2_api.api.api_endpoint
  description = "Base URL for the HTTP API"
}

output "post_summarize_url" {
  value       = "${aws_apigatewayv2_api.api.api_endpoint}/summarize"
  description = "POST endpoint for summarization"
}
