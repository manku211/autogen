module "vpc" {
  source = "../modules/vpc"
  name = "${var.environment}-${var.project_name}"
  cidr_block = var.cidr_block
  enable_dns_support   = var.enable_dns_support
  enable_dns_hostnames = var.enable_dns_hostnames
  tags = merge(
    local.common_tags,
    {
      "kubernetes.io/cluster/${local.eks_cluster_name}" = "shared"
    },
  )
  azs                  = local.selected_azs
  private_subnets      = local.private_subnet_cidrs
  public_subnets       = local.public_subnet_cidrs
  private_subnet_tags = {
    "kubernetes.io/cluster/${local.eks_cluster_name}" = "owned"
    "karpenter.sh/discovery"                          = local.eks_cluster_name
  }
  enable_nat_gateway = var.enable_nat_gateway
  vpc_id = var.vpc_id
}

module "ec2" {
  source = "../modules/ec2"
  create_module_ec2 = var.create_ec2
  vpc_id            = module.vpc.vpc_id
  name = "${var.environment}-${var.project_name}"
  key_name = var.key_name
  depends_on = [module.vpc]

}
