# IAM Role for the scheduler
resource "aws_iam_role" "forecast_scheduler_role" {
name   = "${local.envs["EVENTBRIDGE_SCHEDULER_ROLE_NAME"]}"
assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "scheduler.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
tags = {
  project = "${local.envs["PROJECT"]}"
}
}

# IAM Policy for the scheduler

resource "aws_iam_policy" "invoke_lambda_policy" {
  name        = "${local.envs["EVENTBRIDGE_SCHEDULER_POLICY_NAME"]}"
  description = "A policy that allows a EventBridge scheduler trigger the Lambda function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = ""
        Effect   = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
            "arn:aws:lambda:${local.envs["REGION"]}:${local.envs["AWS_ACCOUNT_ID"]}:function:${local.envs["LAMBDA_FUNCTION_NAME"]}:*",
            "arn:aws:lambda:${local.envs["REGION"]}:${local.envs["AWS_ACCOUNT_ID"]}:function:${local.envs["LAMBDA_FUNCTION_NAME"]}"
        ]
      },
    ]
  })
  tags = {
  project = "${local.envs["PROJECT"]}"
}
}

# Attach policy to Lambda Role
resource "aws_iam_role_policy_attachment" "invoke_lambda_policy_attachement" {
  role       = "${aws_iam_role.forecast_scheduler_role.name}"
  policy_arn = "${aws_iam_policy.invoke_lambda_policy.arn}"
}


# Scheduler
resource "aws_scheduler_schedule" "lambda_forecast_scheduler" {
  name       = "${local.envs["EVENTBRIDGE_SCHEDULER_NAME"]}"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "${local.envs["EVENTBRIDGE_SCHEDULER_CRON"]}"

  target {
    arn      = aws_lambda_function.forecast_lambda.arn
    role_arn = aws_iam_role.forecast_scheduler_role.arn
  }

}