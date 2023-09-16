
resource "aws_ecs_cluster" "cluster" {
  name = "${var.environment}-app-cluster"
}

resource "aws_ecs_service" "service" {
  name = "${var.environment}-app-service"
  cluster = aws_ecs_cluster.cluster.arn
  launch_type = "FARGATE"
  scheduling_strategy = "REPLICA"
  enable_execute_command = true

  deployment_maximum_percent = 200
  deployment_minimum_healthy_percent = 100
  desired_count = 1
  task_definition = aws_ecs_task_definition.app_task.arn

  network_configuration {
    assign_public_ip = true
    security_groups = [aws_security_group.vpc_sec_group.id]
    subnets = [element(aws_subnet.public_subnet.*.id, 0)]
  }
}

resource "aws_ecs_task_definition" "app_task" {
  depends_on = [aws_ecr_repository.backend, aws_db_instance.prod]
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 512
  cpu                      = 256
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
  task_role_arn            = aws_iam_role.ecsTaskExecutionRole.arn
  family                   = "rest-api"
  container_definitions    = jsonencode(
  [
    {
      name : "restapi",
      image : data.aws_ecr_repository.backend.repository_url,
      essential : true,
      environment:[
        {
          "name": "ENVIRONMENT",
          "value": var.environment
        },
        {
          "name": "DATABASE_NAME",
          "value": var.DATABASE_NAME
        },
        {
          "name": "DATABASE_USER",
          "value": var.DATABASE_USER
        },
        {
          "name": "DATABASE_PASSWORD",
          "value": var.DATABASE_PASSWORD
        },
        {
          "name": "DATABASE_HOST",
          "value": aws_db_instance.prod.address
        },
        {
          "name": "DATABASE_PORT",
          "value": var.DATABASE_PORT
        },
        {
          "name": "AFRICASTALKING_API_KEY",
          "value": var.AFRICASTALKING_API_KEY
        },
        {
          "name": "AFRICASTALKING_USERNAME",
          "value": var.AFRICASTALKING_USERNAME
        },
        {
          "name": "AFRICASTALKING_SENDER",
          "value": var.AFRICASTALKING_SENDER
        },
      ]
      portMappings : [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ],
      memory : 512,
      cpu : 256
      logConfiguration: {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-log-group",
          "awslogs-region": var.region,
          "awslogs-stream-prefix": "django-logs"
        }
      }
    }
  ])

}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "TaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
