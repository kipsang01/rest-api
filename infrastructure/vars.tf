variable "environment" {
    type = string
  default = "dev"
}
variable "project_name"{
  description = "name to use in resource names"
  default     = "django-app"
}
variable "region" {
  type = string
  default = "us-east-1"
  description = "AWS Region"
}
variable "AWS_REPO_URL" {
  type = string
  default = ""
}
variable "TFC_AWS_RUN_ROLE_ARN"{

}
variable "TFC_AWS_PROVIDER_AUTH" {

}

variable "vpc_cidr" {
  default     = "10.0.0.0/16"
  description = "CIDR block of the vpc"
}

variable "public_subnets_cidr" {
  type        = list(any)
  default     = ["10.0.0.0/20", "10.0.128.0/20"]
  description = "CIDR block for Public Subnet"
}

variable "private_subnets_cidr" {
  type        = list(any)
  default     = ["10.0.16.0/20", "10.0.144.0/20"]
  description = "CIDR block for Private Subnet"
}

variable "prod_rds_db_name" {
  description = "RDS database name"
  default     = "orders"
}
variable "prod_rds_username" {
  description = "RDS database username"
  default     = "Admin"
}
variable "prod_rds_password" {
  description = "postgres password for production DB"
}
variable "prod_rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t4g.micro"
}

variable "DATABASE_NAME" {
  description = "RDS database name"
  default = ""
}
variable "DATABASE_USER" {
  description = "RDS database username"
  default = ""
}
variable "DATABASE_PASSWORD" {
  description = "RDS database password"
  default = ""
}
variable "DATABASE_URL" {
  default = ""
}
variable "DATABASE_PORT" {
  default = "5342"
}
variable "DATABASE_HOST" {
  default = ""
}
variable "AFRICASTALKING_API_KEY" {
  default = ""
}
variable "AFRICASTALKING_USERNAME" {
  default = ""
}
variable "AFRICASTALKING_SENDER" {
  default = ""
}