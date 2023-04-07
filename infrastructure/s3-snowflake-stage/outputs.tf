output "stage_bucket_arn" {
  description = "ARN of the stage bucket"
  value = "${aws_s3_bucket.stage_bucket.arn}"
}

output "stage_bucket_role_arn" {
  description = "ARN of the created role for the stage bucket"
  value = "${aws_iam_role.snowflake_role.arn}"
}
