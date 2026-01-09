# Phase 3 Testing Guide: Authentication & User Isolation

This guide covers manual testing for Phase 3 (User Story 1 & 4).

## Prerequisites

1. **Set up environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure database**:
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your Neon PostgreSQL connection string
   - Update `JWT_SECRET` with a secure secret (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

3. **Run migrations** (T026):
   ```bash
   cd backend
   alembic upgrade head
   ```

   Expected output:
   ```
   INFO  [alembic.runtime.migration] Running upgrade  -> 001, Create users table
   ```

4. **Start the server**:
   ```bash
   cd backend
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Test T027: Register User

**Endpoint**: `POST http://localhost:8000/auth/register`

**Request**:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securePassword123"
  }'
```

**Expected Response** (201 Created):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "testuser@example.com",
  "created_at": "2026-01-07T12:00:00Z"
}
```

**✅ Pass Criteria**:
- Status code: 201
- Response contains `user_id`, `email`, `created_at`
- User can be found in database

**❌ Failure Cases to Test**:
- Duplicate email returns 400: "Email already exists"
- Empty password returns 422: Validation error
- Password < 8 characters returns 422: Validation error
- Invalid email format returns 422: Validation error

## Test T028: Login User

**Endpoint**: `POST http://localhost:8000/auth/login`

**Request**:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securePassword123"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "testuser@example.com",
    "created_at": "2026-01-07T12:00:00Z"
  }
}
```

**✅ Pass Criteria**:
- Status code: 200
- Response contains `access_token`, `token_type`, `user`
- Token is a valid JWT (can be decoded at https://jwt.io)

**❌ Failure Cases to Test**:
- Wrong password returns 401: "Invalid email or password"
- Non-existent email returns 401: "Invalid email or password"

## Test T029: Access Protected Endpoint Without Token

Since we haven't created any protected endpoints yet, we'll test this by creating a temporary test endpoint.

**Create temporary test file**: `backend/test_protected.py`
```python
from fastapi import FastAPI, Depends
from src.auth.middleware import get_current_user
from src.models.user import User

app = FastAPI()

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "Access granted", "user_id": str(current_user.user_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Test 1: Without Token**
```bash
curl http://localhost:8001/protected
```

**Expected Response** (401 Unauthorized):
```json
{
  "detail": "Not authenticated"
}
```

**✅ Pass Criteria**: Status code 401

**Test 2: With Valid Token**

First, login and extract token:
```bash
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"securePassword123"}' \
  | jq -r '.access_token')
```

Then use token:
```bash
curl http://localhost:8001/protected \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response** (200 OK):
```json
{
  "message": "Access granted",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**✅ Pass Criteria**:
- Status code: 200
- Response contains user information

**Test 3: With Invalid Token**
```bash
curl http://localhost:8001/protected \
  -H "Authorization: Bearer invalid-token-here"
```

**Expected Response** (401 Unauthorized):
```json
{
  "detail": "Invalid or expired token"
}
```

**✅ Pass Criteria**: Status code 401

## Interactive Testing with Swagger UI

FastAPI provides automatic interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints interactively from the browser.

## Summary

All Phase 3 tests passing indicates:
- ✅ User registration works
- ✅ User login returns JWT token
- ✅ JWT tokens are validated correctly
- ✅ Protected endpoints require authentication
- ✅ User isolation is enforced at the authentication layer

**Next**: Proceed to Phase 4 (Task Management) after all tests pass.
