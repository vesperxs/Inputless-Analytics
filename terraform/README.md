# Inputless Analytics - Terraform Deployment

This directory contains Terraform scripts to deploy the Inputless Analytics platform on AWS EC2.

## 🚀 Quick Start

### Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **Terraform installed** (version >= 1.0)
3. **SSH key pair** for EC2 access
4. **Domain name** (optional but recommended)

### 1. Configure Variables

```bash
# Copy the example variables file
cp terraform.tfvars.example terraform.tfvars

# Edit the variables file with your values
vim terraform.tfvars
```

**Required Variables:**
- `ssh_public_key`: Your SSH public key for EC2 access
- `postgres_pass`: Secure PostgreSQL password
- `secret_key`: Django secret key

**Recommended Variables:**
- `domain_name`: Your domain name
- `route53_zone_id`: Route53 hosted zone ID
- `admin_email`: Admin email address

### 2. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

### 3. Access Your Application

After deployment, you'll see output with URLs:
- **Application**: `http://YOUR_IP:3000`
- **Admin Panel**: `http://YOUR_IP:3000/admin/`
- **Grafana**: `http://YOUR_IP:3060`
- **Prometheus**: `http://YOUR_IP:9090`

## 📋 Configuration Options

### Instance Types

| Type | vCPUs | Memory | Storage | Use Case |
|------|-------|--------|---------|----------|
| `t3.medium` | 2 | 4 GB | EBS | Development |
| `t3.large` | 2 | 8 GB | EBS | Production (small) |
| `t3.xlarge` | 4 | 16 GB | EBS | Production (medium) |
| `m5.large` | 2 | 8 GB | EBS | Production (stable) |
| `m5.xlarge` | 4 | 16 GB | EBS | Production (high performance) |

### Storage Options

| Type | IOPS | Throughput | Use Case |
|------|------|------------|----------|
| `gp2` | 3,000 | 250 MB/s | General purpose |
| `gp3` | 3,000+ | 1,000 MB/s | High performance |
| `io1` | 1,000+ | 1,000 MB/s | IOPS intensive |
| `io2` | 1,000+ | 1,000 MB/s | IOPS intensive (latest) |

## 🔧 Customization

### Environment-Specific Deployments

Create different `.tfvars` files for different environments:

```bash
# Development
terraform apply -var-file="dev.tfvars"

# Staging
terraform apply -var-file="staging.tfvars"

# Production
terraform apply -var-file="prod.tfvars"
```

### Custom Domain Setup

1. **Create Route53 Hosted Zone:**
   ```bash
   aws route53 create-hosted-zone --name "yourdomain.com" --caller-reference "inputless-$(date +%s)"
   ```

2. **Update Name Servers:**
   - Copy the name servers from Route53
   - Update your domain registrar

3. **Configure Terraform:**
   ```hcl
   domain_name     = "analytics.yourdomain.com"
   route53_zone_id = "Z1D633PJN98FT9"
   ```

### SSL Certificate Setup

1. **Request Certificate:**
   ```bash
   aws acm request-certificate \
     --domain-name "analytics.yourdomain.com" \
     --validation-method DNS
   ```

2. **Validate Certificate:**
   - Add DNS validation records to Route53
   - Wait for validation to complete

3. **Update Terraform:**
   ```hcl
   enable_ssl          = true
   ssl_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"
   ```

## 🔒 Security Best Practices

### 1. Restrict SSH Access

```hcl
ssh_cidr_blocks = ["YOUR_IP/32"]  # Replace with your IP
```

### 2. Use Secure Passwords

```hcl
postgres_pass = "YourVerySecurePassword123!"
secret_key    = "YourVeryLongDjangoSecretKey1234567890"
```

### 3. Enable Monitoring

```hcl
enable_cloudtrail = true
enable_guardduty  = true
```

### 4. Use Private Subnets (Optional)

For enhanced security, deploy in private subnets with NAT Gateway:

```hcl
enable_nat_gateway = true
```

## 📊 Monitoring & Logging

### CloudWatch Integration

The deployment automatically configures:
- **System metrics**: CPU, memory, disk usage
- **Application logs**: User data, monitoring logs
- **Custom metrics**: Container health, application status

### Grafana Dashboard

Access Grafana at `http://YOUR_IP:3060`:
- Default credentials: `admin/admin`
- Pre-configured dashboards for system and application metrics

### Prometheus Metrics

Access Prometheus at `http://YOUR_IP:9090`:
- Application metrics
- System metrics
- Custom business metrics

## 🔄 Backup & Recovery

### Automated Backups

The deployment includes:
- **Daily backups** at 2 AM UTC
- **S3 storage** for backup files
- **7-day retention** (configurable)
- **Automatic cleanup** of old backups

### Manual Backup

```bash
# SSH into the instance
ssh -i your-key.pem ubuntu@YOUR_IP

# Run backup script
/opt/inputless-analytics/backup.sh
```

### Restore from Backup

```bash
# Download backup from S3
aws s3 cp s3://your-bucket/backups/inputless_backup_20240101_020000.tar.gz ./

# Extract backup
tar -xzf inputless_backup_20240101_020000.tar.gz

# Restart application
docker-compose -f docker-compose.prod.yml restart
```

## 🛠️ Maintenance

### Application Updates

```bash
# SSH into the instance
ssh -i your-key.pem ubuntu@YOUR_IP

# Navigate to application directory
cd /opt/inputless-analytics

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d
```

### Database Migrations

```bash
# Run migrations
docker exec -it Web bash -c "cd /app && python manage.py migrate"

# Create superuser
docker exec -it Web bash -c "cd /app && python manage.py createsuperuser"
```

### Log Management

```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f

# View system logs
tail -f /var/log/user-data.log
tail -f /var/log/inputless-monitor.log
```

## 💰 Cost Optimization

### Spot Instances

For development environments:

```hcl
enable_spot_instances = true
spot_price           = "0.05"
```

### Right-Sizing

Monitor usage and adjust instance types:

```bash
# Check current usage
htop
df -h
docker stats
```

### Scheduled Scaling

For predictable workloads, use scheduled scaling:

```hcl
# Scale down at night
min_size = 0
max_size = 1
```

## 🚨 Troubleshooting

### Common Issues

1. **Application not starting:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs
   ```

2. **Database connection issues:**
   ```bash
   docker exec -it Web bash -c "cd /app && python manage.py dbshell"
   ```

3. **High memory usage:**
   ```bash
   docker stats
   # Consider upgrading instance type
   ```

4. **SSL certificate issues:**
   ```bash
   # Check certificate status
   aws acm describe-certificate --certificate-arn YOUR_CERT_ARN
   ```

### Health Checks

```bash
# Application health
curl http://YOUR_IP:8080/health

# Container status
docker-compose -f docker-compose.prod.yml ps

# System resources
htop
df -h
```

### Support

For issues and questions:
- Check the [main README](../README.md)
- Create an issue on GitHub
- Contact: info@talorik.com

## 📚 Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Inputless Analytics Documentation](../README.md)

## 🔄 Updates

To update the Terraform configuration:

```bash
# Pull latest changes
git pull origin main

# Review changes
terraform plan

# Apply updates
terraform apply
```

## 🗑️ Cleanup

To destroy the infrastructure:

```bash
# Review what will be destroyed
terraform plan -destroy

# Destroy resources
terraform destroy
```

**Warning**: This will permanently delete all resources and data!
