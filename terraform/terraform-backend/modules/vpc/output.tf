output "vpc_id" {
  description = "The ID of the VPC"
  value       =  var.vpc_id == "" ? aws_vpc.vpc[0].id : var.vpc_id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = try(aws_vpc.vpc[*].arn, "")
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = try(aws_vpc.vpc[*].cidr_block, "")
}


output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = try(aws_subnet.private[*].id,"")
}

output "private_subnet_arns" {
  description = "List of ARNs of private subnets"
  value       = try(aws_subnet.private[*].arn,"")
}

output "private_subnets_cidr_blocks" {
  description = "List of cidr_blocks of private subnets"
  value       = try(aws_subnet.private[*].cidr_block,"")
}


output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = try(aws_subnet.public[*].id,"")
}

output "public_subnet_arns" {
  description = "List of ARNs of public subnets"
  value       = try(aws_subnet.public[*].arn,"")
}

output "public_subnets_cidr_blocks" {
  description = "List of cidr_blocks of public subnets"
  value       = try(aws_subnet.public[*].cidr_block,"")
}
