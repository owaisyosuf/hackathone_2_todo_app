# Todo Backend API

A FastAPI backend for the Todo application with authentication and task management.

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL (or Neon PostgreSQL for cloud deployment)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the environment file and configure your settings:
```bash
cp .env.example .env
```

4. Update the `.env` file with your database URL and JWT secret.

### Database Setup

1. Run database migrations:
```bash
alembic upgrade head
```

### Running the Application

Start the development server:
```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Tasks
- `GET /tasks` - Get all user tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task
- `PATCH /tasks/{task_id}/toggle` - Toggle task completion status

All task endpoints require authentication via JWT token in the `Authorization` header.

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `ENVIRONMENT`: Application environment (development/staging/production)

## Project Structure

```
backend/
├── src/
│   ├── api/          # API route handlers
│   ├── auth/         # Authentication middleware and utilities
│   ├── models/       # SQLAlchemy ORM models
│   ├── schemas/      # Pydantic validation schemas
│   ├── services/     # Business logic
│   ├── database.py   # Database configuration
│   └── main.py       # Application entry point
├── alembic/          # Database migrations
├── tests/            # Test files
├── requirements.txt  # Python dependencies
└── .env.example     # Environment variable template
```