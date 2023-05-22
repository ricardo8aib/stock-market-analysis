resource "aws_ecr_repository" "repository" {
  name                 = "${local.envs["ECR_REPO_NAME"]}"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {project = "${local.envs["PROJECT"]}"}
}