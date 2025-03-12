output "function_arns" {
  description = "Map of Lambda function ARNs"
  value       = module.lambda.function_arns
}

output "function_names" {
  description = "Map of Lambda function names"
  value       = module.lambda.function_names
}

output "role_arns" {
  description = "Map of Lambda IAM role ARNs"
  value       = module.lambda.role_arns
} 
