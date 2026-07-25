# 1. ECS Cluster (Konteynerlarımızın koşturulacağı mantıksal küme)
resource "aws_ecs_cluster" "main" {
  name = "customer-churn-cluster"
}

# 2. Security Group (Dışarıdan ve servisler arası trafik izinleri)
resource "aws_security_group" "ecs_sg" {
  name        = "customer-churn-ecs-sg"
  description = "Allow HTTP inbound traffic"
  vpc_id      = aws_default_vpc.default.id

  # Dışarıdan 8000 portuna (API) gelen isteklere izin ver
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Servislerin internete çıkışına izin ver (ECR'dan imaj çekebilmek için)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. ECS Execution Role (Fargate'in ECR'dan imaj çekebilmesi için IAM Rolü)
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

# 4. Task Definition: Customer API
resource "aws_ecs_task_definition" "api" {
  family                   = "customer-churn-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256" # 0.25 vCPU
  memory                   = "512" # 512 MB RAM
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "customer-churn-api"
      image     = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/customer-churn-api:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

# 5. ECS Service: Customer API (Fargate üzerinde sürekli çalışacak servis)
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