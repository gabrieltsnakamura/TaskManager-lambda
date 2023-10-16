terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "taskmanager-bucket"
    key    = "terraform-statefiles/taskManager-lambda.tfstate"
    region = "sa-east-1"
  }
}

provider "aws" {
  region = "sa-east-1"
}


resource "aws_security_group" "lambda_security_group" {
  name_prefix = "lambda-security-group-"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lambda_function" "task_manager_lambda1" {
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda_security_group.id]
  }
  filename         = var.lambda_filename
  function_name    = var.lambda_function_name
  role             = aws_iam_role.task_manager_lambda_role.arn
  handler          = var.lambda_handler
  source_code_hash = filebase64sha256(var.lambda_filename)
  runtime          = "python3.7"
  timeout          = 60

  environment {
    variables = {
      DB_HOST     = "task-manager.c4of4ecvy9np.sa-east-1.rds.amazonaws.com",
      DB_USER     = "admin",
      DB_PASSWORD = "admin1234",
      DB_DATABSE  = "taskmanager",
    }
  }
}
