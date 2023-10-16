data "aws_iam_policy_document" "task_manager_lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ec2:*"
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "task_manager_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "task_manager_lambda_role" {
  name               = "task_manager_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.task_manager_assume_role.json
}

resource "aws_iam_policy" "task_manager_lambda_logging_policy" {
  name        = "task_manager_lambda_logging_policy"
  path        = "/"
  description = "IAM policy for logging"
  policy      = data.aws_iam_policy_document.task_manager_lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "task_manager_lambda_logs" {
  role       = aws_iam_role.task_manager_lambda_role.name
  policy_arn = aws_iam_policy.task_manager_lambda_logging_policy.arn
}
