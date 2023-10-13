terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = var.backend_s3_bucket
    key    = var.backend_s3_key
    region = var.backend_s3_region
  }
}

provider "aws" {
  region = "sa-east-1"
}

resource "aws_lambda_function" "task-manager-lambda" {
    filename         = "task-manager-lambda.zip"
    function_name    = var.lambda_function_name
    role             = aws_iam_role.task-manager-lambda-role.arn
    handler          = var.lambda_handler
    source_code_hash = filebase64sha256("task-manager-lambda.zip")
    runtime          = "python3.7"
    timeout          = 60
}