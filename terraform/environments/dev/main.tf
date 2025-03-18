provider "aws" {
  # region = var.aws_region
  region = local.aws_region
}

locals {
  lambda_config = yamldecode(file(local.lambda_config_path))
}

module "lambda" {
  source = "../../modules/lambda"

  # environment = var.environment
  environment = local.environment
  functions   = local.lambda_config.functions
  
  tags = {
    # Project     = var.project_name
    # Environment = var.environment
    Project     = local.project_name
    Environment = local.environment
    Terraform   = "true"
  }
} 
