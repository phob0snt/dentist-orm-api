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
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/phob0snt/dentist-CRM-API.git
   cd dentist-CRM-API
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost/db_name
# or for MySQL:
# DATABASE_URL=mysql+pymysql://username:password@localhost/db_name
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠 Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

---

**Made with ❤️ for dental