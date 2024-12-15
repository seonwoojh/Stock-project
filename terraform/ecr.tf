resource "aws_ecr_repository" "stock-container" {
  name                 = "stock/producer"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "stock-container_lifecycle" {
  repository = aws_ecr_repository.stock-container.name
  policy     = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Remove untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}