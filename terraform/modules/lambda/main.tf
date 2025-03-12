terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

resource "aws_lambda_function" "this" {
  for_each = var.functions

  filename         = each.value.filename
  function_name    = "${each.key}-${var.environment}"
  role             = aws_iam_role.lambda_role[each.key].arn
  handler          = each.value.handler
  runtime          = each.value.runtime
  timeout          = each.value.timeout
  memory_size      = each.value.memory_size

  environment {
    variables = merge(
      each.value.environment_variables,
      {
        ENV = var.environment
      }
    )
  }

  tags = merge(
    var.tags,
    {
      Environment = var.environment
      Function    = each.key
    }
  )
}

resource "aws_iam_role" "lambda_role" {
  for_each = var.functions
  
  name = "${each.key}-${var.environment}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  for_each = var.functions
  
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role[each.key].name
}

resource "aws_cloudwatch_log_group" "lambda" {
  for_each = var.functions
  
  name              = "/aws/lambda/${each.key}-${var.environment}"
  retention_in_days = var.log_retention_days
} 
