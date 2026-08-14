variable "aws_region" {
  description = "Región de AWS para el despliegue"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Nombre de la aplicación"
  type        = string
  default     = "fastapi-todo"
}