############################################################################################
## SSM 접근을 위한 Role을 생성한다.
resource "aws_iam_role" "ec2_ssm_role" {
  name = "ec2_ssm_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_policy_attachment" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

## Instance Profile을 생성한다.
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  role = aws_iam_role.ec2_ssm_role.name
}

############################################################################################
## Database Data 디렉토리의 EBS 추가 스토리지를 생성한다.
resource "aws_ebs_volume" "Database" {
  availability_zone = module.vpc.azs[0]
  size              = 100
  type              = "gp3"

  tags = {
    Name = " Database EBS"
  }
}

## Database에 추가 스토리지를 마운트한다.
resource "aws_volume_attachment" "database_att" {
  device_name = "/dev/sdb"
  volume_id   = aws_ebs_volume.Database.id
  instance_id = aws_instance.db_instance_ec2.id
}

############################################################################################
## NAT Instance를 생성한다.
resource "aws_instance" "nat_instance_ec2" {
  ami                         = data.aws_ami.amazonLinux.id
  availability_zone           = module.vpc.azs[0]
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.nat_instance_sg.id]
  subnet_id                   = module.vpc.public_subnets[0] ## nat_instance_subnet AZ-a
  source_dest_check           = false
  iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    yum -y install htop rsyslog iptables-services
    timedatectl set-timezone Asia/Seoul
    iptables -A POSTROUTING -t nat -j MASQUERADE -o enX0
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
    systcl -p
  EOF

  tags = {
    Name = "nat-instance"
  }

}

## Kafka Instance를 3개 생성한다.
resource "aws_instance" "kafka_instance_ec2" {
  count                       = 3
  ami                         = data.aws_ami.amazonLinux.id
  availability_zone           = module.vpc.azs[0]
  instance_type               = "t2.medium"
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.kafka_instance_sg.id]
  subnet_id                   = module.vpc.private_subnets[0] ## nat_instance_subnet
  iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    yum -y install htop rsyslog
    timedatectl set-timezone Asia/Seoul
  EOF

  tags = {
    Name = "kafka-instance-${count.index + 1}"
  }
}

## DB Instance를 생성한다.
resource "aws_instance" "db_instance_ec2" {
  ami                         = data.aws_ami.amazonLinux.id
  availability_zone           = module.vpc.azs[0]
  instance_type               = "t2.medium"
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.db_instance_sg.id]
  subnet_id                   = module.vpc.private_subnets[2] ## nat_instance_subnet
  iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    yum -y install htop rsyslog
    timedatectl set-timezone Asia/Seoul
  EOF

  tags = {
    Name = "database-instance"
  }
}