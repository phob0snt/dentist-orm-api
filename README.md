# 🦷 Dentist CRM API

A comprehensive Customer Relationship Management API designed specifically for dental practices. Built with FastAPI and SQLAlchemy, this system helps manage patient leads, appointments, and staff workflows efficiently.

## ✨ Features

- **Lead Management**: Track and manage potential patients
- **Manager System**: Role-based access control for staff
- **Database Integration**: Robust SQLAlchemy ORM with PostgreSQL/MySQL support
- **Environment Configuration**: Secure configuration with environment variables
- **RESTful API**: Clean and intuitive API endpoints
- **Auto Documentation**: Interactive API docs with Swagger/OpenAPI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL database
- Docker
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/phob0snt/dentist-CRM-API.git
   cd dentist-CRM-API
   ```
2. **Configure .env file**
   
3. **Run docker-compose**
   ```bash
   docker-compose up --build
   ```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠 Development

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

---

**Made with ❤️ for dental
