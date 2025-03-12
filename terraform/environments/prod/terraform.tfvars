project_name    = "my-lambda-project"
aws_region      = "ap-northeast-1"
lambda_filename = "../src/function.zip"
lambda_handler  = "lambda_function.lambda_handler"
lambda_runtime  = "python3.11"
lambda_timeout  = 10
lambda_memory_size = 256 

lambda_config = {
  runtime     = "python3.11"
} 
