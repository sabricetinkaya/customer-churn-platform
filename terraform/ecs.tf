# ==========================================
# 1. ECS CLUSTER
# ==========================================
resource "aws_ecs_cluster" "main" {
  name = "customer-churn-cluster"
}

# ==========================================
# 2. SECURITY GROUP
# ==========================================
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

# ==========================================
# 3. IAM EXECUTION ROLE
# ==========================================
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
# 4. TASK DEFINITIONS
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
      environment = [
        { name = "KAFKA_BOOTSTRAP_SERVERS", value = "localhost:9092" }
      ]
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
      environment = [
        { name = "DB_HOST", value = aws_db_instance.postgres.address },
        { name = "DB_PORT", value = "5432" },
        { name = "DB_NAME", value = "churn_db" },
        { name = "DB_USER", value = "postgres" },
        { name = "DB_PASSWORD", value = "ChurnDbPassword2026!" },
        { name = "KAFKA_BOOTSTRAP_SERVERS", value = "localhost:9092" }
      ]
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
      environment = [
        { name = "KAFKA_BOOTSTRAP_SERVERS", value = "localhost:9092" }
      ]
    }
  ])
}

# D) Kafka Service (KRaft Mode)
resource "aws_ecs_task_definition" "kafka" {
  family                   = "customer-churn-kafka"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "kafka"
      image     = "bashj79/kafka-kraft:latest"
      essential = true
      portMappings = [
        { containerPort = 9092, hostPort = 9092 }
      ]
      environment = [
        { name = "KAFKA_CFG_NODE_ID", value = "1" },
        { name = "KAFKA_CFG_PROCESS_ROLES", value = "broker,controller" },
        { name = "KAFKA_CFG_CONTROLLER_QUORUM_VOTERS", value = "1@localhost:9093" },
        { name = "KAFKA_CFG_LISTENERS", value = "PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093" },
        { name = "KAFKA_CFG_ADVERTISED_LISTENERS", value = "PLAINTEXT://127.0.0.1:9092" },
        { name = "KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP", value = "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT" },
        { name = "KAFKA_CFG_CONTROLLER_LISTENER_NAMES", value = "CONTROLLER" },
        { name = "KAFKA_CFG_INTER_BROKER_LISTENER_NAME", value = "PLAINTEXT" }
      ]
    }
  ])
}

# ==========================================
# 5. ECS SERVICES
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

resource "aws_ecs_service" "kafka_service" {
  name            = "customer-churn-kafka-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.kafka.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}