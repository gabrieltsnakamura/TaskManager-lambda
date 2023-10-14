variable "lambda_filename" {
  type        = string
  description = "The name of the lambda zip file"
}

variable "lambda_function_name" {
  type        = string
  description = "The name of the lambda function"
}

variable "lambda_handler" {
  type        = string
  description = "The name of the lambda handler"
  default     = "task-manager-lambda.handler"
}

