# NAT Instance ID 출력
output "nat-instance-private" {
  value = aws_instance.nat_instance_ec2.id
}

# Kafka Instance ID 출력
output "kafka-instance-private" {
  value = aws_instance.kafka_instance_ec2[*].id
}

# DB Instance ID 출력
output "db-instance-private" {
  value = aws_instance.db_instance_ec2.id
}