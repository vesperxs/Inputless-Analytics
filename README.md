# Inputless Analytics - Legal NLP Platform

![Inputless Analytics Logo](/images/logo-black-no-sfondo.png)

A comprehensive **Data Exploration Pipeline for Legal NLP** - an AI-powered SaaS platform designed for legal document analysis, processing, and visualization. Built specifically for Italian legal systems but adaptable to other jurisdictions.

## 🚀 Overview

Inputless Analytics (formerly Inputless Myotis) is a multi-tenant legal document processing platform that enables users to upload, analyze, and interact with legal documents through advanced NLP techniques and interactive visualizations. The platform provides document parsing, entity extraction, graph-based data visualization, and real-time chat communication.

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

### Installation

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

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Giovanni Errico** - *Initial work* - [GitHub](https://github.com/giovanni-errico)
- **Leonardo Trisolini** - *Initial work* - [GitHub](https://github.com/leonardo-trisolini)

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