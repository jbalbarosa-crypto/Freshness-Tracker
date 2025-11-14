# Freshness Tracker - Enhanced Version

A modern web application for tracking meat batch freshness with user authentication, admin dashboard, and QR-based customer checks.

## 🆕 New Features

### Authentication System
- **User Registration**: Create new accounts with email and password
- **User Login**: Secure authentication with JWT tokens
- **User Profiles**: View and update account information
- **Password Hashing**: PBKDF2-based password security

### User Interface Improvements
- **Beautiful Dashboard**: Modern gradient backgrounds and card layouts
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **User Account Menu**: Quick access to profile and logout
- **Landing Page**: Professional homepage for unauthenticated users
- **Interactive Forms**: Real-time validation and error messages
- **Animations**: Smooth transitions and loading states

### Admin Portal Enhancements
- **Collapsible Form**: Clean UI with toggle between form and batch list
- **Success/Error Notifications**: Visual feedback for all operations
- **Batch Management**: Create and manage meat batches easily
- **QR Code Generation**: Automatic QR codes for each batch
- **Product Emojis**: Visual indicators for different meat types

### Freshness Report Improvements
- **Enhanced Status Display**: Color-coded freshness indicators
- **Detailed Information**: Formatted dates and batch information
- **Better Formatting**: Professional card layout with animations
- **Product Icons**: Visual product identification

### Route Protection
- **Protected Routes**: Admin portal and profile only accessible when logged in
- **Public Routes**: Landing page, login, and register accessible to all
- **Loading States**: Smooth loading experience while checking authentication

## 🚀 Getting Started

### Backend Setup

1. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Update Environment Variables** (`.env`):
```env
DATABASE_URL=sqlite:///./freshness.db
HOST=0.0.0.0
PORT=8000
RELOAD=True
CORS_ORIGINS=*
API_TITLE=Freshness Tracker API
API_VERSION=1.0.0
SECRET_KEY=your-secret-key-change-in-production
```

3. **Run Backend**:
```bash
python app.py
```
The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Install Dependencies**:
```bash
cd frontend
npm install
```

2. **Update Environment Variables** (`.env`):
```env
REACT_APP_API_URL=http://localhost:8000
```

3. **Start Frontend**:
```bash
npm start
```
The app will open at `http://localhost:3000`

## 📝 New API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with email and password

### Users
- `GET /users/me` - Get current user information (requires token)
- `PUT /users/me` - Update current user information (requires token)

### Batches (existing, now requires auth)
- `POST /batches/` - Create a new batch
- `GET /batches/` - Get all batches
- `GET /batches/{id}` - Get specific batch details

## 🔐 Authentication Flow

1. User visits the landing page
2. User clicks "Get Started" or "Sign In"
3. User registers or logs in with credentials
4. JWT token is stored in localStorage
5. Token is sent with each API request in Authorization header
6. User can now access admin portal and manage batches
7. User can click profile to view/update account information
8. User can sign out to clear token

## 🎨 Tech Stack

### Frontend
- React 18.2
- React Router 6
- Axios for HTTP requests
- Tailwind CSS for styling
- React QR Code for QR generation

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite database
- PyJWT for authentication
- PBKDF2 for password hashing

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AdminPortal.js      (Admin dashboard)
│   │   ├── FreshnessReport.js   (Customer-facing freshness check)
│   │   ├── Login.js             (Login page)
│   │   ├── Register.js          (Registration page)
│   │   ├── Profile.js           (User profile)
│   │   ├── Navbar.js            (Navigation bar)
│   │   ├── Landing.js           (Landing page)
│   │   └── ProtectedRoute.js    (Route protection)
│   ├── context/
│   │   └── AuthContext.js       (Authentication state)
│   ├── App.js
│   └── index.js
├── .env
├── package.json
└── .gitignore

backend/
├── api/
│   └── routers/
│       ├── batches.py          (Batch endpoints)
│       ├── auth.py             (Authentication endpoints)
│       └── users.py            (User endpoints)
├── controllers/
│   ├── batches.py              (Batch business logic)
│   └── auth.py                 (Authentication logic)
├── models/
│   ├── batch.py                (Batch model)
│   └── user.py                 (User model with password hashing)
├── schemas/
│   ├── batch.py                (Batch validation schemas)
│   └── user.py                 (User validation schemas)
├── database/
│   └── core.py                 (Database configuration)
├── app.py                       (Main application)
├── requirements.txt
├── .env
└── .gitignore
```

## 🔑 Key Features Explained

### JWT Authentication
- Access tokens are created on login/register
- Tokens are stored in browser localStorage
- Tokens are sent with each request via Authorization header
- Tokens expire after 7 days

### Password Security
- Passwords are hashed using PBKDF2
- Each password has a unique salt
- Original passwords are never stored

### Protected Routes
- Certain routes check for valid JWT token
- Unauthenticated users are redirected to login
- Loading state shown while checking authentication

### Responsive Design
- Desktop: Full menu with user dropdown
- Tablet/Mobile: Hamburger menu with mobile layout

## 🛠️ Future Enhancements

- Password reset functionality
- Email verification
- User roles and permissions
- Batch history and analytics
- Export functionality
- Dark mode
- Multi-language support

## 📝 License

This project is private and proprietary.

## 👥 Support

For issues or questions, please contact the development team.
