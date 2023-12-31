
resource "aws_db_instance" "prod" {
  db_name                 = var.DATABASE_NAME
  username                = var.DATABASE_USER
  password                = var.DATABASE_PASSWORD
  port                    = var.DATABASE_PORT
  engine                  = "postgres"
  engine_version          = "15.3"
  instance_class          = var.DATABASE_INSTANCE_CLASS
  allocated_storage       = "20"
  storage_encrypted       = false
  vpc_security_group_ids  = [aws_security_group.rds_prod.id]
  multi_az                = false
  storage_type            = "gp2"
  publicly_accessible     = true
  backup_retention_period = 5
  skip_final_snapshot     = true
}

resource "aws_security_group" "rds_prod" {
  name        = "django-postgres-SG"

  ingress {
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}