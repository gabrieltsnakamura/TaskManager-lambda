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

resource "aws_lambda_function" "task_manager_lambda" {
  filename         = var.lambda_filename
  function_name    = var.lambda_function_name
  role             = aws_iam_role.task_manager_lambda_role.arn
  handler          = var.lambda_handler
  source_code_hash = filebase64sha256("task-manager-lambda.zip")
  runtime          = "python3.7"
  timeout          = 60

  environment {
    variables = {
      DB_HOST = "task-manager.c4of4ecvy9np.sa-east-1.rds.amazonaws.com",
      DB_USER = "admin",
      DB_PASSWORD = "admin1234",
      DB_DATABSE = "taskmanager",
    }
  }
}
