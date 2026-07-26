# 1. RDS için Security Group (Sadece ECS Fargate servislerimizin erişebileceği şekilde)
resource "aws_security_group" "rds_sg" {
  name        = "customer-churn-rds-sg"
  description = "Allow inbound PostgreSQL traffic from ECS Fargate"
  vpc_id      = aws_default_vpc.default.id

  # Sadece ECS Security Group'undan gelen 5432 (Postgres) isteklerine izin ver
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. Free Tier Uyumlu RDS PostgreSQL Veritabanı
resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  max_allocated_storage  = 20
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro" # Free Tier kapsamında ücretsizdir
  db_name                = "churn_db"
  username               = "postgres"
  password               = "ChurnDbPassword2026!" # Üretimde AWS Secrets Manager kullanılır
  parameter_group_name   = "default.postgres15"
  skip_final_snapshot    = true
  publicly_accessible    = false # Dış dünyaya kapalı, sadece VPC içinden erişilebilir

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}

# 3. Veritabanı Bağlantı Adresini Çıktı (Output) Olarak Alalım
output "rds_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "RDS PostgreSQL Endpoint Address"
}