terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

data "local_file" "config" {
  count    = var.enable_environment_variables ? 1 : 0
  filename = "env.json"
}

locals {
  config = var.enable_environment_variables ? jsondecode(data.local_file.config[0].content) : {}
  env  = var.enable_environment_variables ? local.config : {}
}

resource "aws_amplify_app" "example" {
  name                        = var.app_name
  repository                  = var.existing_repo_url
  access_token                 = var.ssm_github_access_token_name
  enable_branch_auto_build    = true
  environment_variables =       var.enable_environment_variables ? local.env : {}
  enable_auto_branch_creation = true
  auto_branch_creation_patterns = [
    "*",
    "*/**",
  ]
  auto_branch_creation_config {
    # Enable auto build for the created branch.
    enable_auto_build = true
  }

  custom_rule {
    source = "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf|map|json)$)([^.]+$)/>"
    status = "200"
    target = "/index.html"
  }
  custom_rule {
    source = "/<*>"
    status = "404"
    target = "/index.html"
  }

}

resource "aws_amplify_branch" "master" {
  app_id           = aws_amplify_app.example.id
  branch_name      = var.branch_name
  enable_auto_build = true
  stage            = "PRODUCTION"
}

resource "aws_amplify_webhook" "master" {
  app_id      = aws_amplify_app.example.id
  branch_name = aws_amplify_branch.master.branch_name
  description = "triggermaster"

  provisioner "local-exec" {
    command = "curl -X POST -d {} '${aws_amplify_webhook.master.url}&operation=startbuild' -H 'Content-Type:application/json'"
  }
}

output "default_domain" {
  description = "The amplify domain (non-custom)."
  value       = aws_amplify_app.example.default_domain
}
output "default_appid" {
  description = "The amplify app_id ."
  value       = aws_amplify_app.example.id
}
