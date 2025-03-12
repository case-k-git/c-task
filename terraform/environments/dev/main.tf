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

# 複数のモジュールを1つのファイルでまとめて管理できる。管理しても可読性はそれほど悪くない
# 他のリポジトリで使う場合は結構便利そう。
# メンテナンスするファイルは増えるので結局モジュールを呼び出しているファイルもシムリンクで管理するだろう
# 総合的に管理するファイルは増えて運用メリットが少ない
# リポジトリを跨いで使う場合には有効かもしれない
