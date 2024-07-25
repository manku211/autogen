terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"

  backend "s3" {
    
    # #  access_key = var.aws_access_key
    # #  bucket = "${var.project_name}-tfstatess"
    # # bucket = "terraform-project-tfstatess"
    # key    = "vpc/terraform.tfstate"
    # region = "us-east-1"
    # encrypt = truesecret_key = var.aws_secret_key
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}