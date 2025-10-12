# Inputless Analytics - Legal NLP Platform

![Inputless Analytics Logo](/images/logo-black-no-sfondo.png)

A comprehensive **Data Exploration Pipeline for Legal NLP** - an AI-powered SaaS platform designed for legal document analysis, processing, and visualization. Built specifically for Italian legal systems but adaptable to other jurisdictions.

## 🚀 Overview

### The "Inputless" Concept

**Inputless Analytics** represents a paradigm shift in legal document analysis - the concept of extracting maximum value from legal documents with minimal manual input. The name "Inputless" doesn't mean no input at all, but rather **intelligent, automated processing** that reduces the traditional manual effort required for legal document analysis.

#### What Makes It "Inputless"?

1. **Automated Document Processing**: Once uploaded, documents are automatically parsed, categorized, and analyzed without manual intervention
2. **Intelligent Entity Extraction**: The system automatically identifies and extracts legal entities, relationships, and key information
3. **Smart Categorization**: Documents are automatically classified by type (Sentenza, Appello, Memoria, etc.) based on content analysis
4. **Dynamic Visualization**: Complex legal relationships are automatically visualized in interactive graphs
5. **Contextual Search**: Advanced NLP enables finding relevant information without complex query construction
6. **Multi-tenant Intelligence**: The system learns and adapts to different legal domains and organizational contexts

#### The Analytics Advantage

The platform transforms raw legal documents into **actionable insights** through:
- **Pattern Recognition**: Identifying recurring legal patterns and precedents
- **Relationship Mapping**: Visualizing connections between cases, parties, and legal concepts
- **Trend Analysis**: Tracking legal developments and changes over time
- **Predictive Insights**: Using historical data to inform future legal strategies

### Platform Capabilities

Inputless Analytics (formerly Inputless Myotis) is a comprehensive multi-tenant legal document processing platform that enables users to upload, analyze, and interact with legal documents through advanced NLP techniques and interactive visualizations. The platform provides document parsing, entity extraction, graph-based data visualization, and real-time chat communication.

#### Core Philosophy

The platform embodies the principle that **legal professionals should focus on strategy and interpretation, not data processing**. By automating the tedious aspects of document analysis, Inputless Analytics empowers legal teams to:

- **Spend more time on legal reasoning** rather than data extraction
- **Discover hidden patterns** in legal documents that might be missed manually
- **Scale their analysis capabilities** across large document collections
- **Collaborate more effectively** through shared visualizations and insights
- **Make data-driven legal decisions** based on comprehensive document analysis

## ✨ Key Features

### 📄 Document Processing
- **Multi-format Support**: PDF, DOC, DOCX, ODT, CSV, XLS, XLSX, PPTX, TXT
- **Intelligent Categorization**: Automatic document type detection (Sentenza, Appello, Memoria, etc.)
- **Text Extraction & Normalization**: Advanced parsing with text cleaning and preprocessing
- **Entity Extraction**: Automatic extraction of persons, locations, legal references, and procedural information

### 🔍 Search & Analytics
- **Full-text Search**: Powered by Whoosh search engine
- **Advanced Filtering**: Multi-scope search capabilities
- **Document Indexing**: Real-time indexing for fast retrieval
- **Analytics Dashboard**: Comprehensive data visualization and statistics

### 📊 Interactive Visualizations
- **Dynamic Graph Layouts**: 
  - Circular Layout
  - Dagre Layout  
  - Sparse Layout
- **Real-time Data Visualization**: Interactive charts and graphs
- **Table View**: Extract, organize, and download processed data
- **Customizable Views**: Reprogrammable interface components

### 💬 Communication & Collaboration
- **System Chat**: Real-time communication platform
- **Multi-tenant Architecture**: Isolated workspaces for different organizations
- **User Management**: Role-based access control

### 🔐 Security & Authentication
- **Two-Factor Authentication (2FA)**: Enhanced security with TOTP and YubiKey support
- **Multi-tenant Security**: Isolated data per tenant
- **Rate Limiting**: Protection against abuse
- **Honeypot Protection**: Anti-bot security measures

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **Django 3.2.10** - Web framework
- **Django Tenants** - Multi-tenancy support
- **Celery** - Asynchronous task processing
- **Redis** - Caching and message broker
- **PostgreSQL** - Primary database
- **ArangoDB** - Graph database for relationships
- **SpaCy 2.3.4** - NLP processing
- **Whoosh** - Full-text search engine

**Frontend:**
- **Webpack 5** - Module bundler
- **AntV G6** - Graph visualization library
- **Bootstrap 5** - UI framework
- **JavaScript Obfuscator** - Code protection

**Infrastructure:**
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy
- **Prometheus** - Monitoring
- **Grafana** - Analytics dashboard
- **Gunicorn** - WSGI server

### System Components

#### Local Development Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django Web    │    │   PostgreSQL    │
│   (Webpack)     │◄──►│   Application   │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Celery        │    │   ArangoDB      │
                       │   Workers       │◄──►│   Graph DB      │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Redis         │    │   Prometheus    │
                       │   Cache/Queue   │    │   Monitoring    │
                       └─────────────────┘    └─────────────────┘
```

#### AWS Production Architecture (Terraform)
```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS VPC (10.0.0.0/16)                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Internet      │  │   EC2 Instance  │  │   EBS Volumes   │ │
│  │   Gateway       │  │   (t3.large)    │  │   (Encrypted)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                    │                    │          │
│           ▼                    ▼                    ▼          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Route53       │  │   Application   │  │   S3 Bucket     │ │
│  │   (DNS)         │  │   Stack         │  │   (Backups)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                    │                    │          │
│           ▼                    ▼                    ▼          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   CloudWatch    │  │   Security      │  │   IAM Roles     │ │
│  │   (Monitoring)  │  │   Groups        │  │   (Permissions) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📱 Screenshots

### Main Dashboard
![Main Screen](/images/main_screen.png)

### User Registration
![Registration Process](/images/registration_process1.png)

### Document Upload Interface
![Upload Interface](/images/upload.png)

### Graph Visualizations

#### Standard Layout
![Graph Visualization](/images/graph.png)

#### Circular Layout
![Circular Layout](/images/graph2.png)

#### Dagre Layout
![Dagre Layout](/images/dagre.png)

#### Sparse Layout
![Sparse Layout](/images/sparse.png)

### Chat System
![Chat Interface 1](/images/chat1.png)
![Chat Interface 2](/images/chat2.png)

### Data Table View
![Table View](/images/table.png)

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js v17.6.0 (for frontend development)
- Git

### Deployment Options

- **🐳 Local Development**: Docker Compose for local testing
- **☁️ AWS Cloud**: Terraform for production deployments
- **🔧 Manual Setup**: Traditional server installation

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Inputless-Analytics.git
   cd Inputless-Analytics
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env.dev
   cp .env.example .env.dev.db
   # Edit the environment files with your configuration
   ```

3. **Build and start the application:**
   ```bash
   # Development environment
   docker-compose --compatibility up --build
   
   # Staging environment
   docker-compose -f docker-compose.staging.yml --compatibility up --build
   
   # Production environment
   docker-compose -f docker-compose.prod.yml --compatibility up --build
   ```

4. **Run database migrations:**
   ```bash
   docker exec -it Web bash
   ./manage.py makemigrations
   ./manage.py migrate
   ```

5. **Access the application:**
   - Web Application: http://localhost:3000
   - Grafana Dashboard: http://localhost:3060
   - Prometheus: http://localhost:9090

### ☁️ AWS Cloud Deployment

For production deployments, use our Terraform infrastructure-as-code setup:

#### Prerequisites for AWS Deployment

- **AWS CLI** configured with appropriate permissions
- **Terraform** (version >= 1.0)
- **SSH key pair** for EC2 access
- **Domain name** (optional but recommended)

#### Quick AWS Deployment

1. **Configure Terraform variables:**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Deploy to AWS:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

3. **Access your deployed application:**
   - Application: `http://YOUR_IP:3000`
   - Admin Panel: `http://YOUR_IP:3000/admin/`
   - Grafana: `http://YOUR_IP:3060`
   - Prometheus: `http://YOUR_IP:9090`

#### AWS Infrastructure Features

- **EC2 Instance** with configurable instance types
- **VPC & Security Groups** with proper network isolation
- **EBS Volumes** for persistent data storage
- **Elastic IP** for static public IP
- **Route53 Integration** for custom domains
- **S3 Bucket** for automated backups
- **CloudWatch** monitoring and logging
- **SSL Certificate** support
- **Auto-scaling** capabilities

For detailed AWS deployment instructions, see the [Terraform Documentation](terraform/README.md).

## 🔧 Configuration

### Environment Variables

Create `.env.dev` and `.env.dev.db` files with the following variables:

```bash
# Database Configuration
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# Django Configuration
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# ArangoDB Configuration
ARANGO_NO_AUTH=1
```

### SSL Certificates (Production)

For production deployment with HTTPS:

1. **Generate Root CA:**
   ```bash
  openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout RootCA.key -out RootCA.pem -subj "/C=US/CN=Example-Root-CA"
  openssl x509 -outform pem -in RootCA.pem -out RootCA.crt
  ```

2. **Generate Domain Certificate:**
   ```bash
   # Create domains.ext file
   echo "authorityKeyIdentifier=keyid,issuer
  basicConstraints=CA:FALSE
  keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
  subjectAltName = @alt_names
  [alt_names]
  DNS.1 = localhost
   DNS.2 = your-domain.com" > domains.ext
   
   # Generate certificate
  openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=localhost.local"
  openssl x509 -req -sha256 -days 1024 -in localhost.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out localhost.crt
  ```
  
## ☁️ Infrastructure as Code (Terraform)

### AWS Deployment Options

We provide comprehensive Terraform scripts for production-ready AWS deployments:

#### 🏗️ Infrastructure Components

| Component | Description | Port | Purpose |
|-----------|-------------|------|---------|
| **EC2 Instance** | Application server | 3000 | Main application |
| **PostgreSQL** | Primary database | 5432 | Data storage |
| **Redis** | Cache & message broker | 6379 | Session & task queue |
| **ArangoDB** | Graph database | 8529 | Relationship data |
| **Grafana** | Monitoring dashboard | 3060 | Metrics visualization |
| **Prometheus** | Metrics collection | 9090 | System monitoring |
| **Nginx** | Reverse proxy | 80/443 | Load balancing |

#### 🚀 Quick Terraform Deployment

```bash
# 1. Configure your deployment
cd terraform
cp terraform.tfvars.example terraform.tfvars

# 2. Edit configuration
vim terraform.tfvars

# 3. Deploy infrastructure
terraform init
terraform plan
terraform apply
```

#### 📋 Required Configuration

**Essential Variables:**
```hcl
# SSH Access
ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC..."

# Database Security
postgres_pass = "YourSecurePassword123!"
secret_key    = "YourDjangoSecretKey..."

# Application
admin_email   = "admin@yourcompany.com"
domain_name   = "analytics.yourcompany.com"  # Optional
```

**Instance Types:**
- **Development**: `t3.medium` (2 vCPU, 4GB RAM)
- **Production**: `t3.large` (2 vCPU, 8GB RAM) or `t3.xlarge` (4 vCPU, 16GB RAM)
- **High Performance**: `m5.xlarge` (4 vCPU, 16GB RAM)

#### 🔒 Security Features

- **VPC Isolation**: Private network with controlled access
- **Security Groups**: Restrictive firewall rules
- **IAM Roles**: Minimal required permissions
- **Encrypted Storage**: EBS volumes with encryption
- **SSL/TLS Support**: Automatic certificate management
- **Backup Encryption**: S3 bucket with encryption

#### 📊 Monitoring & Observability

- **CloudWatch Integration**: System and application metrics
- **Grafana Dashboards**: Pre-configured monitoring
- **Prometheus Metrics**: Custom application metrics
- **Health Checks**: Automated service monitoring
- **Log Aggregation**: Centralized logging system

#### 💰 Cost Optimization

| Environment | Instance Type | Monthly Cost* | Use Case |
|-------------|---------------|---------------|----------|
| Development | t3.medium | ~$30 | Testing & development |
| Staging | t3.large | ~$60 | Pre-production testing |
| Production | t3.xlarge | ~$120 | Production workloads |
| High Performance | m5.xlarge | ~$150 | High-traffic applications |

*Costs are approximate and may vary by region and usage.

#### 🔄 Backup & Recovery

- **Automated Backups**: Daily S3 backups
- **Point-in-time Recovery**: Database snapshots
- **Disaster Recovery**: Multi-AZ deployment options
- **Data Retention**: Configurable retention policies

#### 🌐 Multi-Environment Support

```bash
# Development
terraform apply -var-file="dev.tfvars"

# Staging  
terraform apply -var-file="staging.tfvars"

# Production
terraform apply -var-file="prod.tfvars"
```

For complete Terraform documentation, see [terraform/README.md](terraform/README.md).

## 📊 Monitoring & Analytics

The platform includes comprehensive monitoring through:

- **Prometheus**: Metrics collection
- **Grafana**: Data visualization and dashboards
- **PostgreSQL Exporter**: Database metrics
- **Custom Django Metrics**: Application-specific monitoring

Access monitoring dashboards:
- Grafana: http://localhost:3060
- Prometheus: http://localhost:9090

## 🏢 Multi-Tenancy

The platform supports three tenant types:

1. **Public**: Landing pages and public content
2. **Demo**: Limited functionality for demonstrations
3. **Professional**: Full feature set for paying customers

Each tenant has isolated data and configurations.

## 🔒 Security Features

- **Two-Factor Authentication**: TOTP and YubiKey support
- **Rate Limiting**: API and endpoint protection
- **Honeypot Protection**: Anti-bot security
- **Content Security Policy**: XSS protection
- **Defender**: Login attempt monitoring
- **File Validation**: Secure file upload handling

## 🛠️ Development

### Frontend Development

```bash
cd frontend
npm install
npm run start  # Development server
npm run prod   # Production build
```

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### Infrastructure Development

```bash
# Terraform development
cd terraform
terraform init
terraform plan
terraform apply

# Validate Terraform configuration
terraform validate
terraform fmt

# Destroy infrastructure (careful!)
terraform destroy
```

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test

# Infrastructure tests (if using Terratest)
cd terraform
go test
```

## 🔄 CI/CD Pipeline

### Automated Workflows

Our project includes comprehensive CI/CD pipelines powered by GitHub Actions:

#### 🧪 Continuous Integration (CI)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI** | Push/PR to main/develop | Full application testing |
| **Security** | Weekly + Push/PR | Security vulnerability scanning |
| **Terraform CI** | Push/PR to terraform/ | Infrastructure validation |
| **Documentation** | Push/PR to docs/ | Documentation generation |

#### 🚀 Continuous Deployment (CD)

| Environment | Trigger | Deployment |
|-------------|---------|------------|
| **Staging** | Push to develop | Auto-deploy to staging AWS |
| **Production** | Push to main | Auto-deploy to production AWS |
| **Manual** | Workflow dispatch | On-demand deployment |

#### 🔒 Security Pipeline

- **Dependency Scanning**: Python (Safety, pip-audit) + Node.js (npm audit, Snyk)
- **Code Security**: Bandit, Semgrep, SAST analysis
- **Container Security**: Trivy, Docker Scout vulnerability scanning
- **Infrastructure Security**: Checkov, TFSec, KICS
- **License Compliance**: Automated license checking

#### 📊 Quality Gates

- **Code Quality**: Linting (flake8, ESLint), formatting (black, prettier)
- **Test Coverage**: Backend (pytest) + Frontend (Jest) with coverage reports
- **Security**: All security scans must pass
- **Infrastructure**: Terraform validation and security checks
- **Documentation**: Markdown linting and link checking

#### 🏗️ Infrastructure as Code

- **Terraform Validation**: Format, validate, plan, and apply
- **Cost Estimation**: Infracost integration for cost analysis
- **Security Scanning**: Infrastructure security best practices
- **Multi-Environment**: Separate staging and production configurations

### Pipeline Status

[![CI](https://github.com/your-username/Inputless-Analytics/workflows/Continuous%20Integration/badge.svg)](https://github.com/your-username/Inputless-Analytics/actions)
[![Security](https://github.com/your-username/Inputless-Analytics/workflows/Security%20Scanning/badge.svg)](https://github.com/your-username/Inputless-Analytics/actions)
[![Terraform](https://github.com/your-username/Inputless-Analytics/workflows/Terraform%20CI/badge.svg)](https://github.com/your-username/Inputless-Analytics/actions)
[![Documentation](https://github.com/your-username/Inputless-Analytics/workflows/Documentation/badge.svg)](https://github.com/your-username/Inputless-Analytics/actions)

### Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/your-username/Inputless-Analytics.git
cd Inputless-Analytics

# 2. Set up pre-commit hooks
pip install pre-commit
pre-commit install

# 3. Run local tests
make test

# 4. Run security checks
make security

# 5. Format code
make format
```

### Required Secrets

For the CI/CD pipeline to work, configure these GitHub Secrets:

```bash
# AWS Deployment
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
SSH_PRIVATE_KEY=your_ssh_private_key

# Security Scanning
SNYK_TOKEN=your_snyk_token
INFRACOST_API_KEY=your_infracost_api_key

# Notifications
SLACK_WEBHOOK=your_slack_webhook_url
```

## 📝 API Documentation

The platform provides RESTful APIs for:

- Document upload and processing
- Search and filtering
- User management
- Analytics and reporting
- Chat functionality

API endpoints are available at `/api/` with proper authentication.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Giovanni Errico** - *Initial work* - [GitHub](https://github.com/giovanni-errico)
- **Leonardo Trisolini** - *Initial work* - [GitHub](https://github.com/leonardo-trisolini)

## 🏢 Sponsors

We are grateful to our sponsors who support the development and maintenance of Inputless Analytics:

### Studio Legale Errico

<div align="center">
  <img src="/images/logo_studio2.png" alt="Studio Legale Errico Logo" width="200" height="100">
</div>

**Studio Legale Errico** is a leading Italian law firm specializing in criminal law. Their expertise in criminal document analysis and their commitment to innovation has been instrumental in the development of Inputless Analytics.

- **Website**: [Studio Legale Errico](https://www.studioerrico.legal)
- **Specialization**: Criminal Law
- **Contribution**: Criminal law expertise, legal domain knowledge, testing, and validation of the platform

*Studio Legale Errico provides criminal law expertise and domain knowledge that ensures Inputless Analytics meets the real-world needs of criminal law professionals and legal practitioners.*

## 🌐 Website

Visit our website: [https://inputless-analytics.com](https://inputless-analytics.com)

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact us at info@talorik.com

## 🔮 Roadmap

- [ ] Enhanced AI model integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] API rate limiting improvements
- [ ] Enhanced security features

## ⚠️ Important Notes

- **No AI models included**: This software does not include pre-trained AI models
- **Italian Legal System**: Originally built for Italian legal documents but adaptable
- **Community Development**: The project is open for community contributions
- **Production Deployment**: Requires HTTPS with proper SSL certificates

---

**Built with ❤️ for the legal technology community**