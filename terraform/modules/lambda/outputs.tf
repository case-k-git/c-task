output "function_arns" {
  description = "Map of Lambda function ARNs"
  value       = { for k, v in aws_lambda_function.this : k => v.arn }
}

output "function_names" {
  description = "Map of Lambda function names"
  value       = { for k, v in aws_lambda_function.this : k => v.function_name }
}

output "role_arns" {
  description = "Map of Lambda IAM role ARNs"
  value       = { for k, v in aws_iam_role.lambda_role : k => v.arn }
} 
