variable "aws_region" {
  type        = string
  default     = "ap-south-1" # Mumbai
  description = "AWS region"
}

# OpenRouter API key (used by Lambda)
variable "openrouter_key" {
  type        = string
  sensitive   = true
  description = "OpenRouter API key for summarization"
}
