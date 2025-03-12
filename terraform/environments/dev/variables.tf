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
  default     = "dev"
}

variable "lambda_filename" {
  description = "Path to the Lambda deployment package"
  type        = string
}

variable "lambda_handler" {
  description = "Lambda function handler"
  type        = string
}

variable "lambda_runtime" {
  description = "Lambda function runtime"
  type        = string
  default     = "nodejs18.x"
}

variable "lambda_timeout" {
  description = "Lambda function timeout"
  type        = number
  default     = 3
}

variable "lambda_memory_size" {
  description = "Lambda function memory size"
  type        = number
  default     = 128
}

variable "lambda_config_path" {
  description = "Path to the Lambda configuration YAML file"
  type        = string
  default     = "config/lambda.yaml"
}

variable "lambda_source_dir" {
  description = "Directory containing Lambda function source code"
  type        = string
  default     = "../src"
} 
