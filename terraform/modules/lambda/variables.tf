variable "functions" {
  description = "Map of Lambda functions and their configurations"
  type = map(object({
    filename         = string
    handler          = string
    runtime          = string
    memory_size     = number
    timeout         = number
    environment_variables = map(string)
  }))
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
}

variable "tags" {
  description = "Tags to be applied to resources"
  type        = map(string)
  default     = {}
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention period in days"
  type        = number
  default     = 14
} 
