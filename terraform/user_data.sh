#!/bin/bash
# Inputless Analytics - EC2 User Data Script
# This script sets up the server and deploys the Inputless Analytics application

set -e  # Exit on any error

# Variables from Terraform
PROJECT_NAME="${project_name}"
ENVIRONMENT="${environment}"
DOMAIN_NAME="${domain_name}"
ADMIN_EMAIL="${admin_email}"
POSTGRES_DB="${postgres_db}"
POSTGRES_USER="${postgres_user}"
POSTGRES_PASS="${postgres_pass}"
SECRET_KEY="${secret_key}"
ALLOWED_HOSTS="${allowed_hosts}"
REDIS_URL="${redis_url}"
ARANGO_NO_AUTH="${arango_no_auth}"

# Logging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "Starting Inputless Analytics deployment at $(date)"

# Update system
apt-get update -y
apt-get upgrade -y

# Install required packages
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    git \
    unzip \
    htop \
    vim \
    wget \
    jq \
    awscli

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose
DOCKER_COMPOSE_VERSION="${docker_compose_version}"
curl -L "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Node.js
NODE_VERSION="${node_version}"
curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash -
apt-get install -y nodejs

# Install Python
PYTHON_VERSION="${python_version}"
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update -y
apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-pip python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev

# Create application directory
mkdir -p /opt/inputless-analytics
cd /opt/inputless-analytics

# Clone the repository (replace with your actual repository URL)
# Note: In production, you might want to use a private repository with authentication
git clone https://github.com/your-username/Inputless-Analytics.git .

# Create environment files
cat > .env.dev << EOF
# Database Configuration
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASS}

# Django Configuration
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${ALLOWED_HOSTS},${DOMAIN_NAME}

# Redis Configuration
REDIS_URL=${REDIS_URL}

# ArangoDB Configuration
ARANGO_NO_AUTH=${ARANGO_NO_AUTH}

# Application Configuration
ADMIN_EMAIL=${ADMIN_EMAIL}
PROJECT_NAME=${PROJECT_NAME}
ENVIRONMENT=${ENVIRONMENT}
EOF

cat > .env.dev.db << EOF
# Database Environment
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASS}
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
EOF

# Create production environment files
cp .env.dev .env.prod
cp .env.dev.db .env.prod.db

# Set up data directories
mkdir -p docker-data/appdata
mkdir -p docker-data/postgres_data
mkdir -p docker-data/arangodb_data
mkdir -p docker-data/grafana
mkdir -p logs

# Set proper permissions
chown -R 1000:1000 docker-data/
chmod -R 755 docker-data/

# Create systemd service for the application
cat > /etc/systemd/system/inputless-analytics.service << EOF
[Unit]
Description=Inputless Analytics Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/inputless-analytics
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reload
systemctl enable inputless-analytics.service

# Start Docker
systemctl start docker
systemctl enable docker

# Wait for Docker to be ready
sleep 10

# Build and start the application
cd /opt/inputless-analytics
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 60

# Check if services are running
docker-compose -f docker-compose.prod.yml ps

# Run database migrations
echo "Running database migrations..."
docker exec -it Web bash -c "cd /app && python manage.py migrate" || echo "Migration failed, will retry later"

# Create superuser (optional - you might want to do this manually)
echo "Creating superuser..."
docker exec -it Web bash -c "cd /app && echo 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"admin\", \"${ADMIN_EMAIL}\", \"admin123\") if not User.objects.filter(username=\"admin\").exists() else None'" || echo "Superuser creation skipped"

# Set up log rotation
cat > /etc/logrotate.d/inputless-analytics << EOF
/var/log/user-data.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 root root
}
EOF

# Set up monitoring script
cat > /opt/inputless-analytics/monitor.sh << 'EOF'
#!/bin/bash
# Monitor script for Inputless Analytics

LOG_FILE="/var/log/inputless-monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Checking application status..." >> $LOG_FILE

# Check if Docker is running
if ! systemctl is-active --quiet docker; then
    echo "[$DATE] ERROR: Docker is not running" >> $LOG_FILE
    systemctl start docker
fi

# Check if containers are running
cd /opt/inputless-analytics
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "[$DATE] WARNING: Some containers are not running" >> $LOG_FILE
    docker-compose -f docker-compose.prod.yml ps >> $LOG_FILE
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "[$DATE] WARNING: Disk usage is at ${DISK_USAGE}%" >> $LOG_FILE
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 90" | bc -l) )); then
    echo "[$DATE] WARNING: Memory usage is at ${MEMORY_USAGE}%" >> $LOG_FILE
fi

echo "[$DATE] Health check completed" >> $LOG_FILE
EOF

chmod +x /opt/inputless-analytics/monitor.sh

# Set up cron job for monitoring
echo "*/5 * * * * /opt/inputless-analytics/monitor.sh" | crontab -

# Set up backup script
cat > /opt/inputless-analytics/backup.sh << 'EOF'
#!/bin/bash
# Backup script for Inputless Analytics

BACKUP_DIR="/opt/backups"
DATE=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="inputless_backup_${DATE}.tar.gz"

mkdir -p $BACKUP_DIR

# Create backup
cd /opt/inputless-analytics
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
    --exclude='docker-data/postgres_data' \
    --exclude='docker-data/arangodb_data' \
    --exclude='node_modules' \
    --exclude='.git' \
    .

# Upload to S3 if bucket is configured
if [ ! -z "$S3_BACKUP_BUCKET" ]; then
    aws s3 cp "${BACKUP_DIR}/${BACKUP_FILE}" "s3://${S3_BACKUP_BUCKET}/backups/"
fi

# Clean up old backups (keep last 7 days)
find $BACKUP_DIR -name "inputless_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: ${BACKUP_FILE}"
EOF

chmod +x /opt/inputless-analytics/backup.sh

# Set up daily backup
echo "0 2 * * * /opt/inputless-analytics/backup.sh" | crontab -

# Configure CloudWatch agent for monitoring
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb

# Create CloudWatch config
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << EOF
{
    "metrics": {
        "namespace": "InputlessAnalytics/${PROJECT_NAME}",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait", "cpu_usage_user", "cpu_usage_system"],
                "metrics_collection_interval": 60
            },
            "disk": {
                "measurement": ["used_percent"],
                "metrics_collection_interval": 60,
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"],
                "metrics_collection_interval": 60
            }
        }
    },
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/log/user-data.log",
                        "log_group_name": "/aws/ec2/${PROJECT_NAME}",
                        "log_stream_name": "{instance_id}/user-data.log"
                    },
                    {
                        "file_path": "/var/log/inputless-monitor.log",
                        "log_group_name": "/aws/ec2/${PROJECT_NAME}",
                        "log_stream_name": "{instance_id}/monitor.log"
                    }
                ]
            }
        }
    }
}
EOF

# Start CloudWatch agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
    -s

# Create health check endpoint
cat > /opt/inputless-analytics/health_check.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import json

class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            try:
                # Check if Docker containers are running
                result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                      capture_output=True, text=True)
                containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
                
                # Check if our application containers are running
                app_containers = [c for c in containers if 'inputless' in c.get('Names', '')]
                
                if len(app_containers) >= 3:  # Web, Postgres, Redis, ArangoDB
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'status': 'healthy',
                        'containers': len(app_containers)
                    }).encode())
                else:
                    self.send_response(503)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'status': 'unhealthy',
                        'containers': len(app_containers)
                    }).encode())
            except Exception as e:
                self.send_response(503)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'error': str(e)
                }).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        print(f"Health check server running on port {PORT}")
        httpd.serve_forever()
EOF

chmod +x /opt/inputless-analytics/health_check.py

# Create systemd service for health check
cat > /etc/systemd/system/inputless-health-check.service << EOF
[Unit]
Description=Inputless Analytics Health Check
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/inputless-analytics
ExecStart=/usr/bin/python3 /opt/inputless-analytics/health_check.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable inputless-health-check.service
systemctl start inputless-health-check.service

# Final status check
echo "Deployment completed at $(date)"
echo "Application should be available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000"
echo "Grafana dashboard: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3060"
echo "Prometheus: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):9090"

# Create deployment info file
cat > /opt/inputless-analytics/DEPLOYMENT_INFO.txt << EOF
Inputless Analytics Deployment Information
==========================================

Deployment Date: $(date)
Project Name: ${PROJECT_NAME}
Environment: ${ENVIRONMENT}
Domain: ${DOMAIN_NAME}

Application URLs:
- Main Application: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000
- Admin Panel: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000/admin/
- Grafana: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3060
- Prometheus: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):9090
- Health Check: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080/health

Default Admin Credentials:
- Username: admin
- Password: admin123
- Email: ${ADMIN_EMAIL}

Database Information:
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ArangoDB: localhost:8529

Useful Commands:
- View logs: docker-compose -f docker-compose.prod.yml logs -f
- Restart app: docker-compose -f docker-compose.prod.yml restart
- Stop app: docker-compose -f docker-compose.prod.yml down
- Start app: docker-compose -f docker-compose.prod.yml up -d
- Shell access: docker exec -it Web bash
- Run migrations: docker exec -it Web bash -c "cd /app && python manage.py migrate"
- Create superuser: docker exec -it Web bash -c "cd /app && python manage.py createsuperuser"

Monitoring:
- Health check runs every 5 minutes
- Backups run daily at 2 AM
- Logs are sent to CloudWatch

Next Steps:
1. Change default admin password
2. Configure SSL certificates
3. Set up domain name
4. Configure monitoring alerts
5. Review security settings
EOF

echo "Deployment completed successfully!"
