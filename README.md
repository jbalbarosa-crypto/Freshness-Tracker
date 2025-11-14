# 🥩 Freshness Tracker

A modern, full-stack web application for tracking meat batch freshness with user authentication, admin dashboard, and QR-based customer checks.

## 🌟 Features

### 🔐 Authentication & User Management
- Secure user registration and login with JWT tokens
- Password hashing with PBKDF2 for enhanced security
- User profiles with account management
- Protected routes and role-based access control

### 📊 Admin Dashboard
- Create and manage meat batches
- Automatic QR code generation for each batch
- Beautiful, responsive UI with real-time feedback
- Success/error notifications for all operations
- Visual product indicators with emojis

### 👥 Customer Experience
- Scan QR codes to check batch freshness
- Color-coded freshness indicators:
  - 🟢 **Fresh** (0-2 days)
  - 🟡 **Caution** (3-4 days)
  - 🔴 **Expired** (5+ days)
- Professional freshness report display

### 🎨 User Interface
- Modern gradient backgrounds and card layouts
- Fully responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Interactive forms with real-time validation
- Loading states and visual feedback

## 🚀 Quick Start

### Prerequisites
- **Node.js** 14+ (for frontend)
- **Python** 3.8+ (for backend)
- **npm** (for frontend package management)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will be available at `http://localhost:3000`

### Using the Application

#### For New Users
1. Visit `http://localhost:3000`
2. Click "Get Started"
3. Fill in the registration form
4. You'll be automatically logged in and redirected to the admin portal
5. Start creating batches!

#### For Returning Users
1. Click "Sign In"
2. Enter your credentials
3. Manage your batches in the admin portal

#### For Customers
1. Scan the QR code from a batch
2. View the real-time freshness status
3. Make informed purchase decisions

## 📁 Project Structure

```
Freshness Tracker/
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── AdminPortal.js   # Admin dashboard
│   │   │   ├── FreshnessReport.js
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Profile.js
│   │   │   ├── Navbar.js
│   │   │   ├── Landing.js
│   │   │   └── ProtectedRoute.js
│   │   ├── context/
│   │   │   └── AuthContext.js   # Authentication state
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env
│
└── backend/                     # FastAPI application
    ├── api/
    │   └── routers/             # API endpoints
    │       ├── auth.py          # Authentication
    │       ├── users.py         # User management
    │       └── batches.py       # Batch operations
    ├── controllers/             # Business logic
    │   ├── auth.py
    │   └── batches.py
    ├── models/                  # Database models
    │   ├── user.py
    │   └── batch.py
    ├── schemas/                 # Data validation
    │   ├── user.py
    │   └── batch.py
    ├── database/
    │   └── core.py              # Database config
    ├── app.py                   # Main application
    ├── requirements.txt
    └── .env
```

## 🔑 API Endpoints

### Authentication (Public)
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with email and password

### Users (Protected)
- `GET /users/me` - Get current user information
- `PUT /users/me` - Update current user information

### Batches
- `POST /batches/` - Create a new batch
- `GET /batches/` - Get all batches
- `GET /batches/{id}` - Get specific batch details

### Documentation
- `http://localhost:8000/docs` - Interactive Swagger UI
- `http://localhost:8000/redoc` - ReDoc documentation

## 🛠️ Tech Stack

### Frontend
- **React** 18.2 - UI Framework
- **React Router** 6 - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **React QR Code** - QR code generation

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database (development)
- **PyJWT** - JWT token handling
- **Pydantic** - Data validation

## 🔒 Security Features

### Password Security
- PBKDF2 hashing with salt
- Unique salt per user
- 100,000 iterations for enhanced protection
- Original passwords never stored

### Authentication
- JWT token-based authentication
- 7-day token expiration
- Token verification on every protected request
- Secure token storage in browser localStorage

### Route Protection
- Protected routes require authentication
- Automatic redirects to login for unauthorized access
- Loading states prevent flash of unprotected content

### API Security
- CORS configuration to prevent unauthorized access
- Request validation with Pydantic schemas
- Proper HTTP status codes and error messages

## 📋 Authentication Flow

```
User Registration/Login
    ↓
JWT Token Created & Stored
    ↓
Token Sent with Each Request
    ↓
Token Verified by Backend
    ↓
User Authenticated & Access Granted
```

## 📱 Responsive Design

| Device | Support |
|--------|---------|
| 📱 Mobile | ✅ Fully optimized |
| 📱 Tablet | ✅ Fully optimized |
| 🖥️ Desktop | ✅ Fully optimized |

Mobile features include:
- Hamburger navigation menu
- Touch-friendly buttons and inputs
- Responsive form layouts
- Stack-based card design

## 🎨 Color Scheme

- **Primary Blue** (#3B82F6) - Main actions and highlights
- **Success Green** - Success notifications
- **Warning Yellow** - Caution/warning messages
- **Danger Red** - Errors and expired items

## 🔧 Environment Configuration

### Backend (.env)
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

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend Issues
**Backend won't start?**
- Verify you're in the backend directory
- Ensure port 8000 is available
- Run `pip install -r requirements.txt` to install dependencies
- Check Python version is 3.8 or higher

**Database errors?**
- Delete `freshness.db` to reset the database
- Restart the backend server

### Frontend Issues
**Frontend won't start?**
- Verify you're in the frontend directory
- Delete `node_modules` folder and run `npm install` again
- Ensure port 3000 is available
- Check Node.js version is 14 or higher

**Can't login?**
- Ensure backend is running and accessible
- Check `REACT_APP_API_URL` in `.env` is correct
- Open browser console (F12) to see any errors

## 📚 Additional Documentation

- **[README_FEATURES.md](./README_FEATURES.md)** - Detailed feature documentation
- **[QUICK_START.md](./QUICK_START.md)** - Setup and usage guide
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture overview
- **[DEVELOPMENT_NOTES.md](./DEVELOPMENT_NOTES.md)** - Developer reference
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Project completion summary

## 🚀 Getting Help

### Common Tasks

**Create a batch:**
1. Login to the admin portal
2. Click "+ Add New Batch"
3. Select product type, batch ID, and dates
4. Click "Create Batch"
5. Share the generated QR code with customers

**Check batch freshness:**
1. Scan the QR code from a batch
2. View the real-time freshness status
3. Days on shelf are automatically calculated

**Update profile:**
1. Click the user menu in the top right
2. Select "My Account"
3. Update your information
4. Click "Update Profile"

**Logout:**
1. Click the user menu in the top right
2. Click "Sign Out"
3. You'll be redirected to the landing page

## 🔮 Future Enhancements

- [ ] Password reset functionality
- [ ] Email verification
- [ ] Advanced user roles and permissions
- [ ] Batch history and analytics
- [ ] Export batch data functionality
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## 📊 Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique user email |
| full_name | String | User's full name |
| password_hash | String | Hashed password |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Batches Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| product | String | Product type (Chicken, Beef, Pork, Seafood) |
| batch_identifier | String | Unique batch identifier |
| butcher_date | Date | Date meat was butchered |
| arrival_date | Date | Date meat arrived at facility |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Last update timestamp |

## 📈 Performance

The application is optimized for:
- ✅ Fast page load times
- ✅ Efficient API responses
- ✅ Smooth animations
- ✅ Mobile performance

## 🧪 Testing

To test the application:

1. **Create a test account** with registration form
2. **Create a test batch** in the admin portal
3. **Scan the QR code** to verify freshness display
4. **Update profile** to test account management
5. **Test logout** and login flow

## 📝 License

This project is private and proprietary.

## 👥 Support

For issues, questions, or feedback, please contact the development team.

---

## 🎉 Ready to Get Started?

1. **Clone or download** this repository
2. **Install dependencies** for both frontend and backend
3. **Set up environment files** (.env)
4. **Start the backend** with `python app.py`
5. **Start the frontend** with `npm start`
6. **Open** `http://localhost:3000` in your browser

**That's it! Your freshness tracking application is ready to use.** 🚀

---

**Version:** 2.0.0  
**Status:** Production Ready ✅  
**Last Updated:** November 14, 2025

Made with ❤️ for better meat freshness tracking
