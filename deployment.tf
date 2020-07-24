provider "aws" {
    region = var.region
}

resource "aws_iam_role" "sandman_role" {
    name                = "SandmanRole"
    description         = "Role responsible for starting/stopping Sagemaker instances"
    assume_role_policy  = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Action": "sts:AssumeRole",
              "Principal": {
                  "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": ""
          }
      ]
    }
    EOF
}

resource "aws_iam_role_policy" "sandman_policy" {
    name = "SandmanPolicy"
    role = aws_iam_role.sandman_role.id

    policy = <<-EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Action": [
                    "sagemaker:ListNotebookInstances",
                    "sagemaker:StopNotebookInstance",
                    "sagemaker:StartNotebookInstance",
                    "sagemaker:ListTags",
                    "ec2:DescribeSubnets"
                ],
                "Resource": "*"
            },
            {
                "Sid": "",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:CreateLogGroup"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            }
        ]
    }
  EOF
}

# Sandman Stop

resource "aws_cloudwatch_event_rule" "sandman_stop_rule" {
    name                = "sandman_stop_rule"
    description         = "Stops notebook instances"
    schedule_expression = var.stop_schedule
}

resource "aws_cloudwatch_event_target" "sandman_stop_scheduler" {
    rule =  aws_cloudwatch_event_rule.sandman_stop_rule.name
    arn  =   aws_lambda_function.sandman_stop_instances.arn
}

resource "aws_lambda_permission" "allow_sandman_stop" {
   statement_id = "AllowSandmanStop"
   action = "lambda:InvokeFunction"
   function_name = aws_lambda_function.sandman_stop_instances.function_name
   principal = "events.amazonaws.com"
   source_arn = aws_cloudwatch_event_rule.sandman_stop_rule.arn
}

resource "aws_lambda_function" "sandman_stop_instances" {
  filename          = "sandman_stop.zip"
  function_name     = "sandman_stop_instances"
  role              = aws_iam_role.sandman_role.arn
  handler           = "stop.lambda_handler"
  source_code_hash  = filebase64sha256("sandman_stop.zip")
  runtime           = var.runtime
}

# Sandman Start

resource "aws_cloudwatch_event_rule" "sandman_start_rule" {
    name                = "sandman_start_rule"
    description         = "Starts notebook instances"
    schedule_expression = var.start_schedule
}

resource "aws_cloudwatch_event_target" "sandman_start_scheduler" {
    rule =  aws_cloudwatch_event_rule.sandman_start_rule.name
    arn  =   aws_lambda_function.sandman_start_instances.arn
}

resource "aws_lambda_permission" "allow_sandman_start" {
   statement_id = "AllowSandmanStart"
   action = "lambda:InvokeFunction"
   function_name = aws_lambda_function.sandman_start_instances.function_name
   principal = "events.amazonaws.com"
   source_arn = aws_cloudwatch_event_rule.sandman_start_rule.arn
}

resource "aws_lambda_function" "sandman_start_instances" {
  filename          = "sandman_start.zip"
  function_name     = "sandman_start_instances"
  role              = aws_iam_role.sandman_role.arn
  handler           = "start.lambda_handler"
  source_code_hash  = filebase64sha256("sandman_start.zip")
  runtime           = var.runtime
}
