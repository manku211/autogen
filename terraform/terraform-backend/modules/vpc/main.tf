resource "aws_vpc" "vpc" {
  count                = var.vpc_id == "" ? 1 : 0
  cidr_block           = var.cidr_block
  enable_dns_support   = var.enable_dns_support
  enable_dns_hostnames = var.enable_dns_hostnames
  tags = merge(
    { "Name" = "${var.name}-vpc"},
    var.tags,
  )
}

################################################################################
# Internet Gateway
################################################################################

resource "aws_internet_gateway" "internet_gateway" {
  count = var.vpc_id == "" && var.create_igw && length(var.public_subnets) > 0 ? 1 : 0

  vpc_id = "${aws_vpc.vpc[0].id}"

  tags = merge(
    { "Name" = "${var.name}-ig" },
    var.tags,
    var.igw_tags,
  )
}
################################################################################
# NAT Gateway
################################################################################


resource "aws_eip" "nat" {
  count =   var.vpc_id == "" && var.enable_nat_gateway ? 1 : 0

  vpc = true

  tags = merge(
    {
      "Name" = format(
        "${var.name}-nat-%s",
        element(var.azs, var.enable_nat_gateway ? 0 : count.index),
      )
    },
    var.tags,
    var.nat_eip_tags,
  )
}

resource "aws_nat_gateway" "this" {
   count =   var.vpc_id == "" && var.enable_nat_gateway ? 1 : 0

  allocation_id = "${aws_eip.nat[count.index].id}"
  subnet_id =  "${element(aws_subnet.public.*.id, 0)}"

  tags = merge(
    {
      "Name" = format(
        "${var.name}-nat-%s",
        element(var.azs, 0),
      )
    },
    var.tags,
    var.nat_gateway_tags,
  )

  depends_on = [aws_internet_gateway.internet_gateway]
}


################################################################################
# Public subnet
################################################################################



resource "aws_subnet" "public" {
  count = var.vpc_id == "" ? "${length(var.public_subnets)}" : 0
  vpc_id                          = "${aws_vpc.vpc[0].id}"
  cidr_block                      = var.public_subnets[count.index]
  availability_zone               = "${element(var.azs, count.index)}"
  map_public_ip_on_launch         = var.map_public_ip_on_launch
  tags = merge(
    {
      "Name" = format(
        "${var.name}-${var.public_subnet_suffix}-%s",
        element(var.azs, count.index),
      )
    },
    var.tags,
    var.public_subnet_tags,
  )
}


################################################################################
# Private subnet
################################################################################

resource "aws_subnet" "private" {
   count                   = var.vpc_id == "" ? "${length(var.private_subnets)}" : 0

  vpc_id                          = "${aws_vpc.vpc[0].id}"
  cidr_block                      = var.private_subnets[count.index]
  availability_zone               = "${element(var.azs, count.index)}"
#   availability_zone_id            =  "${element(var.azs,   count.index)}"
  tags = merge(
    {
      "Name" = format(
        "${var.name}-${var.private_subnet_suffix}-%s",
        element(var.azs, count.index),
      )
    },
    var.tags,
    var.private_subnet_tags,
  )
}

################################################################################
#   new route table  of public and private
################################################################################

resource "aws_route_table" "public" {
  count = var.vpc_id == "" && length(var.public_subnets) > 0 ? 1 : 0

  vpc_id = "${aws_vpc.vpc[0].id}"

  tags = merge(
    { "Name" = "${var.name}-${var.public_subnet_suffix}" },
    var.tags,
    var.public_route_table_tags,
  )
}

resource "aws_route_table" "private" {
  count = var.vpc_id == ""  && length(var.private_subnets) > 0 ? 1 : 0

  vpc_id =  "${aws_vpc.vpc[count.index].id}"

  tags = merge(
    {
      "Name" = format(
        "${var.name}-${var.private_subnet_suffix}-%s",
        element(var.azs, count.index),
      )
    },
    var.tags,
    var.private_route_table_tags,
  )
}
################################################################################
#   new route  of public and private
################################################################################

resource "aws_route" "private_nat_gateway" {
  count =  var.vpc_id == ""  && var.enable_nat_gateway ? 1 : 0

  route_table_id         = element(aws_route_table.private[*].id, count.index)
  destination_cidr_block = var.nat_gateway_destination_cidr_block
  nat_gateway_id         = element(aws_nat_gateway.this[*].id, count.index)

  timeouts {
    create = "5m"
  }
}

resource "aws_route" "public_internet_gateway" {
  count =  var.vpc_id == ""  && length(var.public_subnets) > 0 ? 1 : 0

  route_table_id         = aws_route_table.public[0].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.internet_gateway[0].id

  timeouts {
    create = "5m"
  }
}

################################################################################
#  Route table association
################################################################################

resource "aws_route_table_association" "private" {
  count =  var.vpc_id == ""  && length(var.private_subnets) > 0 ? (length(var.private_subnets)) - 1 : 0

  subnet_id = element(aws_subnet.private[*].id, count.index)
  route_table_id = element(
    aws_route_table.private[*].id, count.index)
    
  
}

resource "aws_route_table_association" "public" {
  count = var.vpc_id == ""  && length(var.public_subnets) > 0 ? length(var.public_subnets) : 0

  subnet_id      = element(aws_subnet.public[*].id, count.index)
  route_table_id = element(
    aws_route_table.public[*].id, count.index)
}
