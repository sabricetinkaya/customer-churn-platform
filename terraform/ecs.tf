# 1. ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "customer-churn-cluster"
}

# 2. Security Group
resource "aws_security_group" "ecs_sg" {
  name        = "customer-churn-ecs-sg"
  description = "Allow inbound and outbound traffic for churn services"
  vpc_id      = aws_default_vpc.default.id

  # API dış dünyaya 8000 portundan açık
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Servislerin kendi aralarındaki haberleşmesi için SG içi tüm trafiğe izin ver
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }

  # İnternet çıkışı (ECR imajlarını çekebilmek için)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. ECS Execution Role (ECR'dan imaj çekebilmek için)
resource "aws_iam_role" "ecs_execution_role" {
  name = "customer_churn_ecs_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ==========================================
# 4. TASK DEFINITIONS (3 Servis)
# ==========================================

# A) Customer API
resource "aws_ecs_task_definition" "api" {
  family                   = "customer-churn-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "customer-churn-api"
      image     = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/customer-churn-api:latest"
      essential = true
      portMappings = [{ containerPort = 8000, hostPort = 8000 }]
    }
  ])
}

# B) Persistence Service
resource "aws_ecs_task_definition" "persistence" {
  family                   = "customer-churn-persistence"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "customer-churn-persistence"
      image     = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/customer-churn-persistence:latest"
      essential = true
    }
  ])
}

# C) Prediction Service
resource "aws_ecs_task_definition" "prediction" {
  family                   = "customer-churn-prediction"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "customer-churn-prediction"
      image     = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/customer-churn-prediction:latest"
      essential = true
    }
  ])
}

# ==========================================
# 5. ECS SERVICES (3 Servis)
# ==========================================

resource "aws_ecs_service" "api_service" {
  name            = "customer-churn-api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}

resource "aws_ecs_service" "persistence_service" {
  name            = "customer-churn-persistence-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.persistence.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}

resource "aws_ecs_service" "prediction_service" {
  name            = "customer-churn-prediction-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.prediction.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}