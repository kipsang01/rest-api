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

variable "DATABASE_INSTANCE_CLASS" {
  default = "db.t3.micro"
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
variable "DATABASE_PORT" {
  default = "5342"
}
variable "DATABASE_HOST" {
  default = "localhost"
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