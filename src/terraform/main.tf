############################################################################################
## 모듈을 통해 VPC, Subnet를 생성한다.

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.13.0"

  name = "stock_alert_VPC"
  cidr = "10.100.0.0/16"

  azs = ["ap-northeast-2a", "ap-northeast-2b"] # 가용영역 설정

  public_subnets      = ["10.100.30.0/24", "10.100.40.0/24"]
  public_subnet_names = ["nat-instance-subnet-1", "nat-instance-subnet-2"]
  public_subnet_tags = {
    "Environment" : "dev"
  }

  private_subnets      = ["10.100.100.0/24", "10.100.110.0/24", "10.100.200.0/24", "10.100.210.0/24"] # 서브넷 설정
  private_subnet_names = ["middleware-subnet-1", "middleware-subnet-2", "database-subnet-1", "database-subnet-2"]
  private_subnet_tags = {
    "Environment" : "dev"
  }

  create_igw                          = true  # IGW 비활성화
  manage_default_network_acl          = false # ACL 비활성화
  manage_default_route_table          = false # default rt 비활성화
  manage_default_security_group       = false # default sg 비활성화
  create_multiple_public_route_tables = true  # public subnet rt 각자 생성
}

############################################################################################
### NAT 192.168.222.168 via 인스턴스 ip or 인스턴스 네트워크 인터페이스 
resource "aws_route" "private_to_nat" {
  # for_each = toset(module.vpc.private_route_table_ids)
  # route_table_id         = each.value
  route_table_id         = module.vpc.private_route_table_ids[0]
  destination_cidr_block = "0.0.0.0/0"
  network_interface_id   = aws_instance.nat_instance_ec2.primary_network_interface_id
  depends_on             = [module.vpc.private_subnets]
}

resource "aws_route" "private_to_nat2" {
  route_table_id         = module.vpc.private_route_table_ids[2]
  destination_cidr_block = "0.0.0.0/0"
  network_interface_id   = aws_instance.nat_instance_ec2.primary_network_interface_id
  depends_on             = [module.vpc.private_subnets]
}