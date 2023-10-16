# Create an API Gateway REST API
resource "aws_api_gateway_rest_api" "task_manager_api_gateway" {
  name = "taskmanager-api-gateway"
}

# Create a resource for the Lambda function
resource "aws_api_gateway_resource" "task_manager_api_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.task_manager_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.task_manager_api_gateway.root_resource_id
  path_part   = "user_tasks"
}

# Create a method for the resource
resource "aws_api_gateway_method" "task_manager_api_gateway_method" {
  rest_api_id   = aws_api_gateway_rest_api.task_manager_api_gateway.id
  resource_id   = aws_api_gateway_resource.task_manager_api_gateway_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# Create an integration for the method
resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.task_manager_api_gateway.id
  resource_id             = aws_api_gateway_resource.task_manager_api_gateway_resource.id
  http_method             = aws_api_gateway_method.task_manager_api_gateway_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.task_manager_lambda.invoke_arn
}

resource "aws_lambda_permission" "task_manager_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.task_manager_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.task_manager_api_gateway.execution_arn}/*/*/*"
}

# Create a deployment for the API
resource "aws_api_gateway_deployment" "task_manager_deployment" {
  rest_api_id = aws_api_gateway_rest_api.task_manager_api_gateway.id
  stage_name  = "prod"
}

# Create a stage for the deployment
resource "aws_api_gateway_stage" "task_manager_stage" {
  rest_api_id = aws_api_gateway_rest_api.task_manager_api_gateway.id
  deployment_id = aws_api_gateway_deployment.task_manager_deployment.id
  stage_name = "prod"
}