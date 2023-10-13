variable "backend_s3_bucket" {
  type = string
  description = "The name of the S3 bucket used for Terraform remote state"
  default = "taskmanager-bucket"
}

variable "backend_s3_key" {
  type = string
  description = "The name of the S3 key used for Terraform remote state"
  default = "terraform-statefiles/taskManager-infra.tfstate"
}
  
variable "backend_s3_region" {
  type = string
  description = "The name of the S3 region used for Terraform remote state"
  default = "sa-east-1"
}

variable "lambda_filename" {
  type = string
  description = "The name of the lambda zip file"
}

variable "lambda_function_name" {
  type = string
  description = "The name of the lambda function"
}
  
variable "lambda_handler" {
  type = string
  description = "The name of the lambda handler"
  default = "task-manager-lambda.handler"
}

