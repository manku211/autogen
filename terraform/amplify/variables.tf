variable "aws_access_key" {
  description = "The AWS access key for the AWS provider"
  type        = string
}

variable "aws_secret_key" {
  description = "The AWS secret key for the AWS provider"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "app_name" {
  description = "The name of the Amplify app"
  type        = string
}

variable "existing_repo_url" {
  description = "The URL of the existing repository for the Amplify app"
  type        = string
}


variable "ssm_github_access_token_name" {
  description = "The name of the SSM parameter storing the GitHub access token"
  type        = string
}

variable "enable_environment_variables" {
  description = "Flag to enable environment variables"
  type        = bool
  default     = false
}

variable "environment_variables" {
  description = "Map of environment variables"
  type        = map(string)
  default     = {}
}

variable "branch_name" {
  description = "The name of the branch to be deployed"
  type        = string
}

variable "framework" {
    description = "The name of the framework to be deployed"
  type        = string
  default = "React"
}

variable "platform" {
    description = "The name of the platform to be deployed"
  type        = string
  default = "WEB"
}

variable "build" {
    description = "The build folder name after build"
  type        = string
  default = "dist"
}

variable "app_id" {
  description = "The name of the Amplify app"
  type        = string
  default     = ""
}




