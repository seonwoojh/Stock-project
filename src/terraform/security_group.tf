################################### nat_instance Rule ###################################
resource "aws_security_group" "nat_instance_sg" {
  name        = "nat_instance_sg"
  description = "Security group for nat_instance"
  vpc_id      = module.vpc.vpc_id

  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]] ## middleware Subnet
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[2]] ## db Subnet
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  tags = {
    Name = "nat_instance_sg"
  }
}


################################### kafka_instance Rule ###################################
resource "aws_security_group" "kafka_instance_sg" {
  name        = "kafka_instance_sg"
  description = "Security group for kafka_instance"
  vpc_id      = module.vpc.vpc_id

  ## Kafka 9092
  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]]
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
  }

  ## zookeeper - 2181
  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]]
    from_port   = 2181
    to_port     = 2181
    protocol    = "tcp"
  }

  ## zookeeper - 2888
  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]]
    from_port   = 2888
    to_port     = 2888
    protocol    = "tcp"
  }

  ## zookeeper - 3888
  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]]
    from_port   = 3888
    to_port     = 3888
    protocol    = "tcp"
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"] ## SSM
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  tags = {
    Name = "kafka_instance_sg"
  }
}


# ################################### DataBase_instance Rule ###################################
resource "aws_security_group" "db_instance_sg" {
  name        = "db_instance_sg"
  description = "Security group for db_instance"
  vpc_id      = module.vpc.vpc_id

  ingress {
    cidr_blocks = [module.vpc.private_subnets_cidr_blocks[0]] ## middleware Subnet
    from_port   = 8086
    to_port     = 8086
    protocol    = "tcp"
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"] ## SSM
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  tags = {
    Name = "db_instance_sg"
  }
}