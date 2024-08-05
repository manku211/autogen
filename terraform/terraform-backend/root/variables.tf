variable "access_key" {
  description = "The AWS access key for the AWS provider"
  type        = string
}

variable "secret_key" {
  description = "The AWS secret key for the AWS provider"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "The AWS secret key for the AWS provider"
  type        = string
}

variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
}

variable "enable_dhcp_options" {
  description = "Enable creation of DHCP Options"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in the VPC"
  type        = string
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in the VPC"
  type        = string
  default     = true
}


variable "environment" {
  description = "pls provide the environment"
  type        = string 
}

variable "azs" {
  description = "A list of availability zones names or ids in the region"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "public_subnet_tags" {
  description = "Additional tags for the public subnets"
  type        = map(string)
  default     = {}
}

variable "private_subnet_tags" {
  description = "Additional tags for the private subnets"
  type        = map(string)
  default     = {}
}

variable "public_subnets" {
  description = "A list of public subnets inside the VPC"
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "A list of private subnets inside the VPC"
  type        = list(string)
  default     = []
}

variable "enable_nat_gateway" {
  description = "Should be true if you want to provision NAT Gateways for each of your private networks"
  type        = bool
  default     = true
}

variable "az_count" {
  description = "Number of availability zones to use"
  type        = number
  default     = 2
}

variable "vpc_id" {
  description = "use vpc id to check if vpc present or not"
  type        = string
  default     = ""
}

variable "create_ec2" {
  description = "create ec2 or not"
  type        = bool
  default     = true
}

variable "key_name" {
  description = "key name for the pem file"
  type        = string
  default     = "my_key"
}
