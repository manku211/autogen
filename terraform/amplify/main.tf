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

# data "template_file" "buildspec" {
#   template = file("${path.module}/${var.framework}.tpl")
# }

locals {
  config = var.enable_environment_variables ? jsondecode(data.local_file.config[0].content) : {}
  env  = var.enable_environment_variables ? local.config : {}
  frameworks =var.framework=="Next" ? "Next.js - SSR" : var.framework
  platform = var.framework=="Next"? "WEB_COMPUTE" : var.platform
#   yaml_rg= yamldecode(file("${path.module}/"))
}

resource "aws_amplify_app" "example" {
  count =  var.app_id == "" ? 1 : 0
  name                        = var.app_name
  repository                  = var.existing_repo_url
  access_token                 = var.ssm_github_access_token_name
  enable_branch_auto_build    = true
  # environment_variables =       var.enable_environment_variables ? local.env : {}
  enable_auto_branch_creation = true
  platform =   var.platform
  
  build_spec          = templatefile("${path.module}/${var.framework}.tpl",{ build = var.build })
  auto_branch_creation_patterns = [
    "*",
    "*/**",
  ]
  auto_branch_creation_config {
    # Enable auto build for the created branch.
    enable_auto_build = true
  }

  dynamic "custom_rule" {
    for_each = var.framework != "Next" ? [1] : []
    content {
      source = "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf|map|json)$)([^.]+$)/>"
      status = "200"
      target = "/index.html"
    }
  }


  custom_rule {
    source = "/<*>"
    status = "404"
    target = "/index.html"
  }

}

resource "aws_amplify_branch" "master" {
  count =  var.app_id == "" ? 1 : 0
  app_id           = aws_amplify_app.example[0].id
  branch_name      = var.branch_name
  enable_auto_build = true
  stage            = "PRODUCTION"
  environment_variables =       var.enable_environment_variables ? local.env : {}
}

resource "aws_amplify_branch" "branch" {
  count =  var.app_id != "" ? 1 : 0
  app_id           = var.app_id
  branch_name      = var.branch_name
  enable_auto_build = true
  stage            = "DEVELOPMENT"
  environment_variables =  var.enable_environment_variables ? local.env : {}
}

resource "aws_amplify_webhook" "master" {
  count =  var.app_id == "" ? 1 : 0
  app_id      = aws_amplify_app.example[0].id
  branch_name = aws_amplify_branch.master[0].branch_name
  description = "${var.branch_name}-trigger"

  provisioner "local-exec" {
    command = "curl -X POST -d {} '${aws_amplify_webhook.master[0].url}&operation=startbuild' -H 'Content-Type:application/json'"
  }
}


resource "aws_amplify_webhook" "branch" {
  count =  var.app_id != "" ? 1 : 0
  app_id      = var.app_id
  branch_name = aws_amplify_branch.branch[0].branch_name
  description = "${var.branch_name}-trigger"

  provisioner "local-exec" {
    command = "curl -X POST -d {} '${aws_amplify_webhook.branch[0].url}&operation=startbuild' -H 'Content-Type:application/json'"
  }
}

output "default_domain" {
  description = "The amplify domain (non-custom)."
  value       =  var.app_id == "" ? aws_amplify_app.example[0].default_domain : aws_amplify_branch.branch[0].custom_domains
}
output "default_appid" {
  description = "The amplify app_id ."
  value       =  var.app_id == "" ? aws_amplify_app.example[0].id : var.app_id
}