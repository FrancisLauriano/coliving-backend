resource "aws_lambda_function" "person_service" {
  function_name = "coliving-backend-person-service"
  handler       = "handler.get_person"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/../app/zipped_function.zip"
}

resource "aws_api_gateway_rest_api" "person_api" {
  name = "Person API"
}

resource "aws_api_gateway_resource" "person" {
  rest_api_id = aws_api_gateway_rest_api.person_api.id
  parent_id   = aws_api_gateway_rest_api.person_api.root_resource_id
  path_part   = "person"
}

resource "aws_api_gateway_method" "get_person" {
  rest_api_id   = aws_api_gateway_rest_api.person_api.id
  resource_id   = aws_api_gateway_resource.person.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.person_api.id
  resource_id = aws_api_gateway_resource.person.id
  http_method = aws_api_gateway_method.get_person.http_method
  type        = "AWS_PROXY"
  uri         = aws_lambda_function.person_service.invoke_arn
}
