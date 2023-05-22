variable "profile" {
  type        = string
  description = "AWS profile to run Terraform"
}

variable "region" {
  type        = string
  description = "Region to use for provisioning"
}

variable "project" {
  type        = string
  description = "Project tag for the resources"
}

variable "acl" {
  type        = string
  description = "The canned ACL to apply"
}

locals {
  envs = { for tuple in regexall("(.*)=(.*)", file("../../.env")) : tuple[0] => sensitive(tuple[1]) }
}