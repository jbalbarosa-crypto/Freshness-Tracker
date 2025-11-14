# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRESHNESS TRACKER                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐        ┌──────────────────────────┐
│       FRONTEND           │        │       BACKEND            │
│    (React + Tailwind)    │        │  (FastAPI + SQLAlchemy)  │
└──────────────────────────┘        └──────────────────────────┘

```

## Frontend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  App.js (Main Router)                                        │
│  ├─ AuthProvider (Context)                                   │
│  │  └─ Navbar (Navigation)                                   │
│  │                                                            │
│  └─ Routes:                                                   │
│     ├─ Public Routes:                                         │
│     │  ├─ / (Landing)                                        │
│     │  ├─ /login (Login)                                     │
│     │  ├─ /register (Register)                               │
│     │  └─ /batch/:id (FreshnessReport)                       │
│     │                                                         │
│     └─ Protected Routes:                                      │
│        ├─ /admin (AdminPortal) → Protected                  │
│        └─ /profile (Profile) → Protected                    │
│                                                               │
├─ Context:                                                     │
│  └─ AuthContext                                              │
│     ├─ user state                                             │
│     ├─ login()                                                │
│     ├─ register()                                             │
│     ├─ logout()                                               │
│     └─ updateProfile()                                        │
│                                                               │
├─ Components:                                                  │
│  ├─ Navbar                                                    │
│  ├─ Landing                                                   │
│  ├─ Login                                                     │
│  ├─ Register                                                  │
│  ├─ AdminPortal                                              │
│  ├─ FreshnessReport                                          │
│  ├─ Profile                                                   │
│  └─ ProtectedRoute                                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘

```

## Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  app.py (Main Application)                                   │
│  ├─ CORS Middleware                                          │
│  ├─ Request/Response Handlers                                │
│  └─ Route Includes                                           │
│                                                               │
│  API Routers:                                                │
│  ├─ auth.py                                                  │
│  │  ├─ POST /auth/register                                   │
│  │  └─ POST /auth/login                                      │
│  │                                                            │
│  ├─ users.py                                                 │
│  │  ├─ GET /users/me (Protected)                             │
│  │  ├─ PUT /users/me (Protected)                             │
│  │  └─ get_current_user() (Dependency)                       │
│  │                                                            │
│  └─ batches.py                                               │
│     ├─ POST /batches/                                        │
│     ├─ GET /batches/                                         │
│     └─ GET /batches/{id}                                     │
│                                                               │
│  Controllers:                                                │
│  ├─ auth.py                                                  │
│  │  ├─ register_user()                                       │
│  │  ├─ login_user()                                          │
│  │  ├─ create_access_token()                                 │
│  │  ├─ verify_token()                                        │
│  │  └─ get_user_by_id()                                      │
│  │                                                            │
│  └─ batches.py                                               │
│     ├─ create_batch()                                        │
│     ├─ get_batches()                                         │
│     └─ get_batch()                                           │
│                                                               │
│  Models (SQLAlchemy ORM):                                     │
│  ├─ user.py                                                  │
│  │  ├─ id                                                     │
│  │  ├─ email (unique)                                         │
│  │  ├─ full_name                                              │
│  │  ├─ password_hash                                          │
│  │  └─ timestamps                                             │
│  │                                                            │
│  └─ batch.py                                                 │
│     ├─ id                                                     │
│     ├─ product                                                │
│     ├─ batch_identifier                                       │
│     ├─ dates                                                  │
│     └─ calculated fields                                      │
│                                                               │
│  Schemas (Pydantic):                                          │
│  ├─ user.py                                                  │
│  │  ├─ UserBase                                              │
│  │  ├─ UserCreate                                            │
│  │  ├─ UserResponse                                          │
│  │  ├─ LoginRequest/Response                                 │
│  │  └─ RegisterRequest/Response                              │
│  │                                                            │
│  └─ batch.py                                                 │
│     ├─ BatchCreate                                           │
│     └─ BatchResponse                                         │
│                                                               │
│  Database:                                                    │
│  └─ core.py                                                  │
│     ├─ Database URL config                                   │
│     ├─ SQLAlchemy engine                                     │
│     ├─ Session factory                                       │
│     └─ get_db() dependency                                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘

```

## Authentication Flow

```
┌─ REGISTRATION ─────────────────────────────────────────┐
│                                                         │
│  User enters:                                           │
│  ├─ Email                                               │
│  ├─ Full Name                                           │
│  └─ Password                                            │
│         │                                               │
│         ▼                                               │
│  Frontend: POST /auth/register                         │
│         │                                               │
│         ▼                                               │
│  Backend:                                               │
│  ├─ Validate input                                      │
│  ├─ Check email not duplicate                           │
│  ├─ Hash password (PBKDF2)                              │
│  ├─ Create User in DB                                   │
│  └─ Generate JWT Token                                  │
│         │                                               │
│         ▼                                               │
│  Return: {token, user}                                  │
│         │                                               │
│         ▼                                               │
│  Frontend:                                              │
│  ├─ Store token in localStorage                         │
│  ├─ Set user in context                                 │
│  └─ Redirect to /admin                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─ LOGIN ────────────────────────────────────────────────┐
│                                                         │
│  User enters:                                           │
│  ├─ Email                                               │
│  └─ Password                                            │
│         │                                               │
│         ▼                                               │
│  Frontend: POST /auth/login                            │
│         │                                               │
│         ▼                                               │
│  Backend:                                               │
│  ├─ Find user by email                                  │
│  ├─ Verify password hash                                │
│  ├─ Generate JWT Token                                  │
│  └─ Return {token, user}                                │
│         │                                               │
│         ▼                                               │
│  Frontend:                                              │
│  ├─ Store token in localStorage                         │
│  ├─ Set user in context                                 │
│  └─ Redirect to /admin                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─ PROTECTED REQUEST ────────────────────────────────────┐
│                                                         │
│  Frontend makes request:                                │
│  GET /users/me                                          │
│  Headers: {                                             │
│    Authorization: "Bearer {jwt_token}"                  │
│  }                                                      │
│         │                                               │
│         ▼                                               │
│  Backend:                                               │
│  ├─ Extract token from header                           │
│  ├─ Verify token signature                              │
│  ├─ Verify token not expired                            │
│  ├─ Extract user_id from token                          │
│  ├─ Get user from DB                                    │
│  └─ Return user data                                    │
│         │                                               │
│         ▼                                               │
│  Frontend receives user data                            │
│                                                         │
└─────────────────────────────────────────────────────────┘

```

## Data Flow - Create Batch

```
┌─────────────────────────────────────────────────────────┐
│                  CREATE BATCH FLOW                      │
└─────────────────────────────────────────────────────────┘

Admin fills form:
┌─────────────┐
│ Product     │
│ Batch ID    │
│ Dates       │
└─────────────┘
       │
       ▼
React state: formData
       │
       ▼
Submit button clicked
       │
       ▼
Frontend: axios.post(/batches/, formData)
with header: Authorization: Bearer {token}
       │
       ▼
Backend: routers/batches.py
  ├─ Get current_user (middleware)
  ├─ Validate data (Pydantic schema)
  ├─ Create Batch model instance
  ├─ Save to database
  └─ Return created batch
       │
       ▼
Frontend:
  ├─ Get response
  ├─ Show success message
  ├─ Clear form
  ├─ Fetch updated batch list
  └─ Update state
       │
       ▼
Display batch with QR code

```

## Data Flow - Check Freshness (Customer)

```
┌─────────────────────────────────────────────────────────┐
│               CUSTOMER FRESHNESS CHECK                  │
└─────────────────────────────────────────────────────────┘

Customer scans QR code
       │
       ▼
URL: /batch/{id}
       │
       ▼
Frontend: /components/FreshnessReport.js
  ├─ Extract batch ID from URL
  ├─ axios.get(/batches/{id})
  └─ Display loading state
       │
       ▼
Backend: routers/batches.py
  ├─ Get batch by ID
  ├─ Calculate days_on_shelf
  └─ Return batch data
       │
       ▼
Frontend receives data:
{
  id: 1,
  product: "Chicken",
  batch_identifier: "BATCH-001",
  butcher_date: "2025-11-10",
  arrival_date: "2025-11-12",
  days_on_shelf: 2
}
       │
       ▼
Calculate freshness status:
  ├─ days_on_shelf <= 2 → Fresh (🥩)
  ├─ days_on_shelf 3-4 → Caution (⚠️)
  └─ days_on_shelf >= 5 → Expired (⛔)
       │
       ▼
Display beautiful freshness report

```

## Directory Tree

```
Freshness Tracker/
├── README_FEATURES.md
├── QUICK_START.md
├── CHANGES_SUMMARY.md
├── DEVELOPMENT_NOTES.md
├── IMPLEMENTATION_CHECKLIST.md
├── PROJECT_SUMMARY.md
├── ARCHITECTURE.md (this file)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdminPortal.js
│   │   │   ├── FreshnessReport.js
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Profile.js
│   │   │   ├── Navbar.js
│   │   │   ├── Landing.js
│   │   │   └── ProtectedRoute.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── package.json
│   └── tailwind.config.js
│
└── backend/
    ├── api/
    │   └── routers/
    │       ├── __init__.py
    │       ├── auth.py
    │       ├── users.py
    │       └── batches.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── auth.py
    │   └── batches.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── batch.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── user.py
    │   └── batch.py
    ├── database/
    │   ├── __init__.py
    │   └── core.py
    ├── .env
    ├── .gitignore
    ├── app.py
    ├── requirements.txt
    └── freshness.db (created at runtime)

```

## Technology Stack

```
FRONTEND:
├─ React 18.2 (UI Framework)
├─ React Router 6 (Navigation)
├─ Axios (HTTP Client)
├─ Tailwind CSS (Styling)
├─ React QR Code (QR Generation)
└─ Context API (State Management)

BACKEND:
├─ FastAPI (Web Framework)
├─ Uvicorn (ASGI Server)
├─ SQLAlchemy (ORM)
├─ SQLite (Database)
├─ PyJWT (JWT Tokens)
├─ Pydantic (Validation)
├─ Python-dotenv (Config)
└─ PBKDF2 (Password Hashing)

DEPLOYMENT:
├─ Frontend: Vercel/Netlify/AWS
├─ Backend: Heroku/AWS/DigitalOcean
├─ Database: SQLite → PostgreSQL (production)
└─ SSL: Let's Encrypt

```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  SECURITY LAYERS                        │
└─────────────────────────────────────────────────────────┘

Layer 1: HTTPS/SSL
└─ All traffic encrypted

Layer 2: CORS
└─ Only allowed origins can access

Layer 3: Authentication
├─ Email + Password required
└─ JWT token validation

Layer 4: Authorization
├─ Token verified on every request
└─ User context extracted

Layer 5: Password Security
├─ PBKDF2 hashing
├─ Unique salt per user
└─ 100,000 iterations

Layer 6: Input Validation
├─ Frontend validation
├─ Pydantic schemas
└─ Type checking

Layer 7: Error Handling
├─ No sensitive info in errors
├─ Generic error messages
└─ Proper HTTP status codes

```

## Deployment Architecture (Future)

```
┌────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                      │
└────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌────────┐        ┌────────┐       ┌─────────┐
    │Vercel/ │        │ CDN    │       │Analytics│
    │Netlify │        │ Cache  │       │ Service │
    └────────┘        └────────┘       └─────────┘
         │
         │ HTTPS
         │
         ▼
    ┌────────────────────────────────────────┐
    │    API Gateway / Load Balancer         │
    └────────────────────────────────────────┘
         │
         │ HTTPS
         │
         ▼
    ┌────────────────────────────────────────┐
    │   FastAPI Backend (Multiple Instances) │
    │   - Gunicorn/Uvicorn                   │
    │   - Auto-scaling                       │
    │   - Load balanced                      │
    └────────────────────────────────────────┘
         │
         │ SQL
         │
         ▼
    ┌────────────────────────────────────────┐
    │   PostgreSQL Database                  │
    │   - Master/Slave replication           │
    │   - Automated backups                  │
    │   - Connection pooling                 │
    └────────────────────────────────────────┘

```

---

**This architecture is designed for:**
- ✅ Scalability
- ✅ Security
- ✅ Performance
- ✅ Maintainability
- ✅ Easy deployment
