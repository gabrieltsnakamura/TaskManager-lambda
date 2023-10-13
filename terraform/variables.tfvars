# Terraform backend configuration
backend_s3_bucket = "taskmanager-bucket"
backend_s3_key = "erraform-statefiles/taskManager-infra.tfstate"
backend_s3_region = "sa-east-1"

# Lambda configuration
lambda_function_name = "task-manager-lambda"
lambda_handler = "task-manager-lambda.handler"
