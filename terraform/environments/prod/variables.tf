variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "lambda_config_path" {
  description = "Path to the Lambda configuration YAML file"
  type        = string
  default     = "config/lambda.yaml"
}

variable "lambda_runtime" {
  description = "The runtime environment for the Lambda function"
  type        = string
  default     = "python3.11"
} 
