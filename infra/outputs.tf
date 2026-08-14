output "ecr_repository_url" {
  description = "URL del repositorio ECR para hacer push de la imagen de Docker"
  value       = aws_ecr_repository.app_repo.repository_url
}