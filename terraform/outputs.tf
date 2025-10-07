# Inputless Analytics - Terraform Outputs
# Define important resource information to display after deployment

# Instance Information
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.inputless_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.inputless_eip.public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.inputless_server.private_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.inputless_server.public_dns
}

# Network Information
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.inputless_vpc.id
}

output "subnet_id" {
  description = "ID of the subnet"
  value       = aws_subnet.inputless_subnet.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.inputless_sg.id
}

# Application URLs
output "application_url" {
  description = "URL to access the Inputless Analytics application"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "http://${aws_eip.inputless_eip.public_ip}:3000"
}

output "admin_url" {
  description = "URL to access the Django admin panel"
  value       = var.domain_name != "" ? "https://${var.domain_name}/admin/" : "http://${aws_eip.inputless_eip.public_ip}:3000/admin/"
}

output "grafana_url" {
  description = "URL to access Grafana dashboard"
  value       = var.enable_grafana ? (var.domain_name != "" ? "https://${var.domain_name}:3060" : "http://${aws_eip.inputless_eip.public_ip}:3060") : "Grafana disabled"
}

output "prometheus_url" {
  description = "URL to access Prometheus monitoring"
  value       = var.enable_prometheus ? (var.domain_name != "" ? "https://${var.domain_name}:9090" : "http://${aws_eip.inputless_eip.public_ip}:9090") : "Prometheus disabled"
}

# Database Information
output "postgres_connection_info" {
  description = "PostgreSQL connection information"
  value = {
    host     = aws_instance.inputless_server.private_ip
    port     = 5432
    database = var.postgres_db
    username = var.postgres_user
    # Password is sensitive and not shown in output
  }
  sensitive = false
}

output "redis_connection_info" {
  description = "Redis connection information"
  value = {
    host = aws_instance.inputless_server.private_ip
    port = 6379
    url  = "redis://${aws_instance.inputless_server.private_ip}:6379/0"
  }
}

output "arangodb_connection_info" {
  description = "ArangoDB connection information"
  value = {
    host = aws_instance.inputless_server.private_ip
    port = 8529
    url  = "http://${aws_instance.inputless_server.private_ip}:8529"
  }
}

# Storage Information
output "ebs_volume_id" {
  description = "ID of the EBS volume for data storage"
  value       = aws_ebs_volume.inputless_data.id
}

output "ebs_volume_size" {
  description = "Size of the EBS volume in GB"
  value       = aws_ebs_volume.inputless_data.size
}

# Backup Information
output "backup_bucket_name" {
  description = "Name of the S3 bucket for backups"
  value       = var.create_backup_bucket ? aws_s3_bucket.inputless_backups[0].bucket : "Backup bucket not created"
}

# SSH Connection Information
output "ssh_connection_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i your-key.pem ubuntu@${aws_eip.inputless_eip.public_ip}"
}

# Docker Commands
output "docker_commands" {
  description = "Useful Docker commands for managing the application"
  value = {
    view_logs     = "docker-compose logs -f"
    restart_app   = "docker-compose restart"
    stop_app      = "docker-compose down"
    start_app     = "docker-compose up -d"
    view_status   = "docker-compose ps"
    shell_access  = "docker exec -it Web bash"
  }
}

# Environment Information
output "environment_info" {
  description = "Environment and project information"
  value = {
    project_name = var.project_name
    environment  = var.environment
    region       = var.aws_region
    instance_type = var.instance_type
  }
}

# Security Information
output "security_info" {
  description = "Security-related information"
  value = {
    security_group_id = aws_security_group.inputless_sg.id
    key_pair_name     = aws_key_pair.inputless_key.key_name
    iam_role_arn      = aws_iam_role.inputless_ec2_role.arn
  }
}

# Monitoring Information
output "monitoring_info" {
  description = "Monitoring and logging information"
  value = {
    cloudwatch_log_group = aws_cloudwatch_log_group.inputless_logs.name
    log_retention_days   = var.log_retention_days
    grafana_enabled      = var.enable_grafana
    prometheus_enabled   = var.enable_prometheus
  }
}

# Cost Information
output "estimated_monthly_cost" {
  description = "Estimated monthly cost breakdown (approximate)"
  value = {
    ec2_instance = "$${var.instance_type == "t3.large" ? "60" : "varies"} per month"
    ebs_storage  = "$${var.ebs_volume_size * 0.1} per month"
    eip          = "$3.65 per month"
    data_transfer = "Varies based on usage"
    total_estimate = "$${var.instance_type == "t3.large" ? "65" : "varies"} - $${var.instance_type == "t3.large" ? "100" : "varies"} per month"
  }
}

# Deployment Status
output "deployment_status" {
  description = "Deployment status and next steps"
  value = {
    status = "Deployment completed successfully"
    next_steps = [
      "1. SSH into the instance: ${aws_eip.inputless_eip.public_ip}",
      "2. Check application status: docker-compose ps",
      "3. Access the application: ${var.domain_name != "" ? "https://${var.domain_name}" : "http://${aws_eip.inputless_eip.public_ip}:3000"}",
      "4. Run database migrations: docker exec -it Web bash -c './manage.py migrate'",
      "5. Create superuser: docker exec -it Web bash -c './manage.py createsuperuser'",
      "6. Configure SSL certificates if needed",
      "7. Set up monitoring alerts in Grafana"
    ]
  }
}

# Resource Tags
output "resource_tags" {
  description = "Tags applied to resources"
  value = {
    project     = var.project_name
    environment = var.environment
    managed_by  = "terraform"
    created_at  = timestamp()
  }
}

# Configuration Summary
output "configuration_summary" {
  description = "Summary of the deployed configuration"
  value = {
    instance_type     = var.instance_type
    storage_size      = "${var.ebs_volume_size}GB"
    database          = "PostgreSQL + ArangoDB + Redis"
    monitoring        = var.enable_grafana ? "Grafana + Prometheus" : "Basic CloudWatch"
    ssl_enabled       = var.enable_ssl
    backup_enabled    = var.create_backup_bucket
    multi_tenant      = true
    authentication    = "Django + 2FA support"
  }
}
