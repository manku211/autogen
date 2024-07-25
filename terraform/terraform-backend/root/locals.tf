locals {
  common_tags = tomap({
    "project" = var.project_name,
    "environment" = var.environment
  })
  eks_cluster_name = "${var.environment}-${var.project_name}-eks"
  bucket = "${var.project_name}-tfstatess"
  
  selected_azs = slice(var.azs, 0, var.az_count)
  existing_az_count = length(local.selected_azs)
  num_private_subnets = local.existing_az_count + 1
  num_public_subnets  = local.existing_az_count
  cidr_count   = local.num_private_subnets + local.num_public_subnets
  subnet_bits = ceil(log(local.cidr_count, 2))
  private_subnet_cidrs = [ for netnumber in range(0, local.num_private_subnets): cidrsubnet(var.cidr_block, local.subnet_bits, netnumber) ]
  public_subnet_cidrs = [ for netnumber in range(local.num_private_subnets,local.cidr_count): cidrsubnet(var.cidr_block, local.subnet_bits, netnumber) ]

}