# Inputless Analytics - Terraform Variables
# Define all configurable variables with descriptions and default values

# General Configuration
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "inputless-analytics"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

# Networking Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "ssh_cidr_blocks" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# EC2 Configuration
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.large"
  validation {
    condition = can(regex("^[a-z][0-9]+\\.[a-z]+$", var.instance_type))
    error_message = "Instance type must be a valid AWS instance type."
  }
}

variable "root_volume_size" {
  description = "Size of root EBS volume in GB"
  type        = number
  default     = 20
  validation {
    condition     = var.root_volume_size >= 8
    error_message = "Root volume size must be at least 8 GB."
  }
}

variable "ebs_volume_size" {
  description = "Size of additional EBS volume for data in GB"
  type        = number
  default     = 100
  validation {
    condition     = var.ebs_volume_size >= 20
    error_message = "EBS volume size must be at least 20 GB."
  }
}

variable "ebs_volume_type" {
  description = "Type of EBS volume"
  type        = string
  default     = "gp3"
  validation {
    condition     = contains(["gp2", "gp3", "io1", "io2"], var.ebs_volume_type)
    error_message = "EBS volume type must be one of: gp2, gp3, io1, io2."
  }
}

# SSH Configuration
variable "ssh_public_key" {
  description = "SSH public key for EC2 access"
  type        = string
  default     = ""
  validation {
    condition     = length(var.ssh_public_key) > 0
    error_message = "SSH public key must be provided."
  }
}

# Domain Configuration
variable "domain_name" {
  description = "Domain name for the application (optional)"
  type        = string
  default     = ""
}

variable "route53_zone_id" {
  description = "Route53 hosted zone ID for domain (required if domain_name is set)"
  type        = string
  default     = ""
}

# Application Configuration
variable "admin_email" {
  description = "Admin email for the application"
  type        = string
  default     = "admin@example.com"
  validation {
    condition     = can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.admin_email))
    error_message = "Admin email must be a valid email address."
  }
}

# Database Configuration
variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "inputless_analytics"
  sensitive   = false
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "postgres"
  sensitive   = false
}

variable "postgres_pass" {
  description = "PostgreSQL password"
  type        = string
  default     = "CHANGE_ME_SECURE_PASSWORD"
  sensitive   = true
}

# Django Configuration
variable "secret_key" {
  description = "Django secret key"
  type        = string
  default     = "CHANGE_ME_DJANGO_SECRET_KEY"
  sensitive   = true
}

variable "allowed_hosts" {
  description = "Django ALLOWED_HOSTS (comma-separated)"
  type        = string
  default     = "localhost,127.0.0.1"
}

# Redis Configuration
variable "redis_url" {
  description = "Redis connection URL"
  type        = string
  default     = "redis://localhost:6379/0"
}

# ArangoDB Configuration
variable "arango_no_auth" {
  description = "Disable ArangoDB authentication"
  type        = string
  default     = "1"
}

# Monitoring Configuration
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
  validation {
    condition     = var.log_retention_days >= 1 && var.log_retention_days <= 3653
    error_message = "Log retention days must be between 1 and 3653."
  }
}

# Backup Configuration
variable "create_backup_bucket" {
  description = "Create S3 bucket for backups"
  type        = bool
  default     = true
}

# SSL Configuration
variable "ssl_certificate_arn" {
  description = "ARN of SSL certificate for HTTPS (optional)"
  type        = string
  default     = ""
}

variable "enable_ssl" {
  description = "Enable SSL/HTTPS"
  type        = bool
  default     = false
}

# Scaling Configuration
variable "min_size" {
  description = "Minimum number of instances in Auto Scaling Group"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of instances in Auto Scaling Group"
  type        = number
  default     = 3
}

variable "desired_capacity" {
  description = "Desired number of instances in Auto Scaling Group"
  type        = number
  default     = 1
}

# Tags
variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

# Cost Optimization
variable "enable_spot_instances" {
  description = "Use spot instances for cost optimization"
  type        = bool
  default     = false
}

variable "spot_price" {
  description = "Maximum spot price (only used if enable_spot_instances is true)"
  type        = string
  default     = "0.05"
}

# Security Configuration
variable "enable_cloudtrail" {
  description = "Enable CloudTrail for API logging"
  type        = bool
  default     = false
}

variable "enable_guardduty" {
  description = "Enable GuardDuty for threat detection"
  type        = bool
  default     = false
}

# Backup Configuration
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
  validation {
    condition     = var.backup_retention_days >= 1 && var.backup_retention_days <= 365
    error_message = "Backup retention days must be between 1 and 365."
  }
}

variable "backup_schedule" {
  description = "Cron expression for backup schedule"
  type        = string
  default     = "0 2 * * *" # Daily at 2 AM
}

# Performance Configuration
variable "enable_enhanced_monitoring" {
  description = "Enable enhanced monitoring for EC2 instances"
  type        = bool
  default     = true
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed monitoring (1-minute intervals)"
  type        = bool
  default     = false
}

# Network Configuration
variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = false
}

variable "enable_vpc_endpoints" {
  description = "Enable VPC endpoints for AWS services"
  type        = bool
  default     = false
}

# Application Configuration
variable "docker_compose_version" {
  description = "Docker Compose version to install"
  type        = string
  default     = "2.20.0"
}

variable "node_version" {
  description = "Node.js version for frontend"
  type        = string
  default     = "17.6.0"
}

variable "python_version" {
  description = "Python version for backend"
  type        = string
  default     = "3.9"
}

# Resource Limits
variable "memory_limit" {
  description = "Memory limit for Docker containers (in MB)"
  type        = number
  default     = 4096
}

variable "cpu_limit" {
  description = "CPU limit for Docker containers (in cores)"
  type        = number
  default     = 2
}

# Feature Flags
variable "enable_grafana" {
  description = "Enable Grafana monitoring dashboard"
  type        = bool
  default     = true
}

variable "enable_prometheus" {
  description = "Enable Prometheus metrics collection"
  type        = bool
  default     = true
}

variable "enable_nginx" {
  description = "Enable Nginx reverse proxy"
  type        = bool
  default     = true
}

variable "enable_ssl_termination" {
  description = "Enable SSL termination at load balancer"
  type        = bool
  default     = false
}
