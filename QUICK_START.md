# Quick Start Guide

## Prerequisites
- Node.js 14+ (for frontend)
- Python 3.8+ (for backend)
- npm or yarn (for frontend package management)

## Quick Setup

### 1. Backend Setup (PowerShell)

```powershell
cd "c:\Users\Administrator\Downloads\Freshness Tracker\backend"

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
```

Backend will run at: `http://localhost:8000`

### 2. Frontend Setup (New Terminal)

```powershell
cd "c:\Users\Administrator\Downloads\Freshness Tracker\frontend"

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

Frontend will open at: `http://localhost:3000`

## Using the App

### First Time Users

1. Open `http://localhost:3000`
2. Click "Get Started" button
3. Fill in the registration form
4. You'll be logged in automatically
5. Start adding batches in the Admin Portal

### Login

1. Click "Sign In"
2. Enter your email and password
3. You'll be logged in

### Admin Portal

1. Click "+ Add New Batch"
2. Fill in:
   - Product type (Chicken, Beef, Pork, Seafood)
   - Batch identifier (e.g., "BATCH-001")
   - Butcher date
   - Arrival date
3. Click "Create Batch"
4. Each batch will show a QR code
5. Share QR codes with customers

### Customer Freshness Check

1. Customer scans the QR code
2. Gets redirected to: `http://localhost:3000/batch/{id}`
3. Sees real-time freshness status:
   - 🥩 Green (Fresh) - 0-2 days
   - ⚠️ Yellow (Caution) - 3-4 days
   - ⛔ Red (Expired) - 5+ days

### Manage Account

1. Click the user menu (top right)
2. Click "My Account"
3. Update your name and email
4. Click "Sign Out" to logout

## Troubleshooting

### Backend won't start
- Make sure you're in the backend directory
- Check that port 8000 is not in use
- Verify all dependencies installed: `pip install -r requirements.txt`

### Frontend won't start
- Make sure you're in the frontend directory
- Delete `node_modules` folder and run `npm install` again
- Check that port 3000 is not in use

### Can't login
- Make sure backend is running
- Check that REACT_APP_API_URL in frontend/.env is correct
- Open browser DevTools console to see any errors

### Database issues
- Delete `freshness.db` file from backend folder to reset
- Restart backend

## API Documentation

Once backend is running, view interactive API docs:
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## Environment Files

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

For production, update:
- Backend: Change `SECRET_KEY` to a strong random value
- Frontend: Change `REACT_APP_API_URL` to production backend URL
