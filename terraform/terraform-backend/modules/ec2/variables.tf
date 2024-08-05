variable "create_module_ec2" {
  description = "set true or false to create ec2 or not"
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "use vpc id to check if vpc present or not"
  type        = string
  default     = ""
}

variable "name" {
  description = "Name to be used on all the resources as identifier"
  type        = string
  default     = ""
}

variable "instance_type" {
  description = "The type of instance to create"
  type        = string
  default     = "t2.medium"
}

variable "ami_id" {
  description = "The ID of the AMI to use for the instance"
  type        = string
  default     = "ami-03972092c42e8c0ca"  # Example AMI, change to your desired AMI
}

variable "tags" {
  description = "A map of tags to assign to the instance"
  type        = map(string)
  default     = {}
}



variable "cidr_blocks" {
  description = "The CIDR blocks for ingress rules"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
variable "ports" {
  description = "List of ports for ingress rules"
  type        = list(number)
  default     = [80, 443, 22]
}


variable "root_block_override" {
  description = "Whether to override the root block device settings"
  type        = bool
  default     = true
}

variable "root_block_delete_on_termination" {
  description = "Whether to delete the root block device on termination"
  type        = bool
  default     = true
}

variable "root_block_volume_type" {
  description = "Type of the root block volume"
  type        = string
  default     = "gp3"
}

variable "root_block_iops" {
  description = "IOPS for the root block volume"
  type        = number
  default     = null
}

# variable "root_block_kms_key_id" {
#   description = "KMS key ID for the root block volume encryption"
#   type        = string
#   default     = null
# }

# variable "root_block_throughput" {
#   description = "Throughput for the root block volume"
#   type        = number
#   default     = null
# }

variable "root_block_volume_size" {
  description = "Size of the root block volume"
  type        = number
  default     = 8
}

variable "key_name" {
  description = "key name for the pem file"
  type        = string
  default     = "my_key"
}
