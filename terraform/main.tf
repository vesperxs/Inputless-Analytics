# Inputless Analytics - Terraform Infrastructure
# This script deploys the Inputless Analytics platform on AWS EC2

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-lts-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# VPC and Networking
resource "aws_vpc" "inputless_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
    Project     = "Inputless Analytics"
  }
}

resource "aws_internet_gateway" "inputless_igw" {
  vpc_id = aws_vpc.inputless_vpc.id

  tags = {
    Name        = "${var.project_name}-igw"
    Environment = var.environment
  }
}

resource "aws_subnet" "inputless_subnet" {
  vpc_id                  = aws_vpc.inputless_vpc.id
  cidr_block              = var.subnet_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.project_name}-subnet"
    Environment = var.environment
  }
}

resource "aws_route_table" "inputless_rt" {
  vpc_id = aws_vpc.inputless_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.inputless_igw.id
  }

  tags = {
    Name        = "${var.project_name}-rt"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "inputless_rta" {
  subnet_id      = aws_subnet.inputless_subnet.id
  route_table_id = aws_route_table.inputless_rt.id
}

# Security Groups
resource "aws_security_group" "inputless_sg" {
  name_prefix = "${var.project_name}-sg"
  vpc_id      = aws_vpc.inputless_vpc.id

  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_cidr_blocks
    description = "SSH access"
  }

  # HTTP access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }

  # HTTPS access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS access"
  }

  # Application port
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Inputless Analytics application"
  }

  # Webpack dev server
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Webpack dev server"
  }

  # Grafana
  ingress {
    from_port   = 3060
    to_port     = 3060
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Grafana dashboard"
  }

  # Prometheus
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Prometheus monitoring"
  }

  # PostgreSQL
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "PostgreSQL database"
  }

  # Redis
  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "Redis cache"
  }

  # ArangoDB
  ingress {
    from_port   = 8529
    to_port     = 8529
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "ArangoDB graph database"
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = {
    Name        = "${var.project_name}-sg"
    Environment = var.environment
  }
}

# IAM Role for EC2 instance
resource "aws_iam_role" "inputless_ec2_role" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-ec2-role"
    Environment = var.environment
  }
}

resource "aws_iam_instance_profile" "inputless_ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.inputless_ec2_role.name
}

# Attach policies to the role
resource "aws_iam_role_policy_attachment" "inputless_ssm_policy" {
  role       = aws_iam_role.inputless_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Key Pair
resource "aws_key_pair" "inputless_key" {
  key_name   = "${var.project_name}-key"
  public_key = var.ssh_public_key

  tags = {
    Name        = "${var.project_name}-key"
    Environment = var.environment
  }
}

# EBS Volume for persistent data
resource "aws_ebs_volume" "inputless_data" {
  availability_zone = data.aws_availability_zones.available.names[0]
  size              = var.ebs_volume_size
  type              = var.ebs_volume_type
  encrypted         = true

  tags = {
    Name        = "${var.project_name}-data-volume"
    Environment = var.environment
  }
}

# EC2 Instance
resource "aws_instance" "inputless_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name              = aws_key_pair.inputless_key.key_name
  vpc_security_group_ids = [aws_security_group.inputless_sg.id]
  subnet_id             = aws_subnet.inputless_subnet.id
  iam_instance_profile  = aws_iam_instance_profile.inputless_ec2_profile.name

  user_data = templatefile("${path.module}/user_data.sh", {
    project_name    = var.project_name
    environment     = var.environment
    domain_name     = var.domain_name
    admin_email     = var.admin_email
    postgres_db     = var.postgres_db
    postgres_user   = var.postgres_user
    postgres_pass   = var.postgres_pass
    secret_key      = var.secret_key
    allowed_hosts   = var.allowed_hosts
    redis_url       = var.redis_url
    arango_no_auth  = var.arango_no_auth
  })

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name        = "${var.project_name}-server"
    Environment = var.environment
    Project     = "Inputless Analytics"
  }
}

# Attach EBS volume
resource "aws_volume_attachment" "inputless_data_attachment" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.inputless_data.id
  instance_id = aws_instance.inputless_server.id
}

# Elastic IP
resource "aws_eip" "inputless_eip" {
  instance = aws_instance.inputless_server.id
  domain   = "vpc"

  tags = {
    Name        = "${var.project_name}-eip"
    Environment = var.environment
  }
}

# Route53 Record (if domain is provided)
resource "aws_route53_record" "inputless_domain" {
  count   = var.domain_name != "" ? 1 : 0
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"
  ttl     = 300
  records = [aws_eip.inputless_eip.public_ip]
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "inputless_logs" {
  name              = "/aws/ec2/${var.project_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "${var.project_name}-logs"
    Environment = var.environment
  }
}

# S3 Bucket for backups (optional)
resource "aws_s3_bucket" "inputless_backups" {
  count  = var.create_backup_bucket ? 1 : 0
  bucket = "${var.project_name}-backups-${random_id.bucket_suffix[0].hex}"

  tags = {
    Name        = "${var.project_name}-backups"
    Environment = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  count       = var.create_backup_bucket ? 1 : 0
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "inputless_backups_versioning" {
  count  = var.create_backup_bucket ? 1 : 0
  bucket = aws_s3_bucket.inputless_backups[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "inputless_backups_encryption" {
  count  = var.create_backup_bucket ? 1 : 0
  bucket = aws_s3_bucket.inputless_backups[0].id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
