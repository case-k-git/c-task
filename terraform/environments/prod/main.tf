provider "aws" {
  region = var.aws_region
}

locals {
  lambda_config = yamldecode(file(var.lambda_config_path))
}

module "lambda" {
  source = "../../modules/lambda"

  environment = var.environment
  functions   = local.lambda_config.functions
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
    Terraform   = "true"
  }
} 
