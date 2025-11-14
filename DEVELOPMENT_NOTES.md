# Development Notes

## Recent Updates (v2.0.0)

### What Was Added

#### Frontend
- Complete authentication system with registration and login
- User account management and profile page
- Beautiful, modern UI with Tailwind CSS
- Responsive navigation bar with user menu
- Protected routes for authenticated users only
- Professional landing page
- Enhanced admin dashboard with better UX
- Improved freshness report display
- Authentication context for state management

#### Backend
- User model with password hashing (PBKDF2)
- JWT authentication with token expiration
- User registration endpoint
- User login endpoint
- User profile endpoints (get/update)
- Route protection middleware
- Comprehensive error handling

### How Authentication Works

1. **User Registers**
   - Email, password, and full name required
   - Password is hashed with PBKDF2
   - Salt is randomly generated for each user
   - User data saved to database

2. **User Logs In**
   - Email and password provided
   - Password verified against hash
   - JWT token generated (valid for 7 days)
   - Token returned to frontend
   - Token stored in localStorage

3. **Protected Requests**
   - Token sent in Authorization header
   - Backend verifies token signature
   - User ID extracted from token
   - Request processed for that user

4. **Token Expiration**
   - Token is valid for 7 days
   - After expiration, user must login again
   - New token generated on next login

### File Organization

**Frontend Components:**
```
components/
├── AdminPortal.js      - Batch management dashboard
├── FreshnessReport.js  - Customer freshness checker
├── Login.js            - Login page
├── Register.js         - Registration page
├── Profile.js          - User profile management
├── Navbar.js           - Navigation with user menu
├── Landing.js          - Home/landing page
└── ProtectedRoute.js   - Route authentication wrapper

context/
└── AuthContext.js      - Auth state management
```

**Backend Modules:**
```
api/routers/
├── auth.py      - Auth endpoints
├── users.py     - User endpoints
└── batches.py   - Batch endpoints

controllers/
├── auth.py      - Auth logic
└── batches.py   - Batch logic

models/
├── user.py      - User database model
└── batch.py     - Batch database model

schemas/
├── user.py      - User validation schemas
└── batch.py     - Batch validation schemas
```

### Database Schema

**Users Table:**
- id (Primary Key)
- email (Unique, Indexed)
- full_name
- password_hash (PBKDF2 hashed)
- created_at (Timestamp)
- updated_at (Timestamp)

**Batches Table:**
(Already existing)
- id
- product
- batch_identifier
- butcher_date
- arrival_date

### API Contract

**Request Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Response Format:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2025-11-14T10:00:00"
}
```

### Frontend State Management

**AuthContext provides:**
- `user` - Current user object or null
- `loading` - Boolean for initial auth check
- `error` - Error message if auth failed
- `isAuthenticated` - Boolean if user is logged in
- `login(email, password)` - Login function
- `register(email, password, full_name)` - Register function
- `logout()` - Logout function
- `updateProfile(updates)` - Update user info

### Environment Variables

**Backend (.env):**
- `DATABASE_URL` - Database connection string
- `HOST` - Server host
- `PORT` - Server port
- `RELOAD` - Auto-reload on changes
- `CORS_ORIGINS` - Allowed origins
- `API_TITLE` - API documentation title
- `API_VERSION` - API version
- `SECRET_KEY` - JWT signing key (change in production!)

**Frontend (.env):**
- `REACT_APP_API_URL` - Backend API URL

### Routing

**Public Routes:**
- `/` - Landing page
- `/login` - Login page
- `/register` - Registration page
- `/batch/:id` - Freshness report (public, no auth needed)

**Protected Routes:**
- `/admin` - Admin dashboard (auth required)
- `/profile` - User profile (auth required)

**Route Behavior:**
- Unauthenticated users accessing protected routes → Redirected to login
- Loading state shown while checking authentication
- Automatic redirect after successful login/logout

### Security Considerations

1. **Password Storage**
   - Never store plain passwords
   - Use PBKDF2 with salt
   - Salt unique per user
   - 100,000 iterations for hashing

2. **Token Security**
   - Tokens stored in localStorage (XSS vulnerable)
   - Use httpOnly cookies in production
   - Tokens expire after 7 days
   - Token verified on every protected request

3. **CORS**
   - Currently allows all origins (*)
   - Should be restricted in production
   - Only allow trusted frontend domains

4. **Input Validation**
   - Email validation on registration/login
   - Password length requirement (6+ chars)
   - Form validation on frontend
   - Server-side validation in backend

### Performance Tips

1. **Frontend**
   - Token checked on app mount
   - User state persists across page refreshes
   - Loading state prevents route jumps
   - Protected routes minimize API calls

2. **Backend**
   - JWT verification is fast
   - Database indexes on email for quick lookups
   - SQLite for simple deployments (upgrade to PostgreSQL later)

### Testing Scenarios

**Registration:**
1. Valid email and password → Success
2. Duplicate email → Error message
3. Short password → Error message
4. Empty fields → Validation error

**Login:**
1. Valid credentials → Success, redirected to admin
2. Invalid email → Error message
3. Wrong password → Error message
4. Unregistered email → Error message

**Protected Routes:**
1. No token → Redirect to login
2. Invalid token → Redirect to login
3. Valid token → Access granted
4. Expired token → Redirect to login on next action

### Common Issues & Solutions

**"Cannot find module" errors:**
- Solution: Run `npm install` in frontend folder
- Solution: Run `pip install -r requirements.txt` in backend

**CORS errors:**
- Solution: Make sure backend CORS_ORIGINS includes frontend URL
- Solution: Check backend is running

**"Authorization failed" errors:**
- Solution: Check token in localStorage (Dev Tools)
- Solution: Verify SECRET_KEY is same in backend

**Blank Admin page:**
- Solution: Check if user is authenticated
- Solution: Check browser console for errors

**Database locked:**
- Solution: Delete freshness.db and restart backend
- Solution: Check no other process is accessing database

### Future Improvements

1. **Security**
   - Move tokens to httpOnly cookies
   - Add CSRF protection
   - Implement rate limiting
   - Add password strength requirements

2. **Features**
   - Password reset/change
   - Email verification
   - User roles (admin, manager, viewer)
   - Batch history and analytics
   - Batch deletion/editing

3. **Performance**
   - Migrate to PostgreSQL
   - Add caching layer
   - Optimize database queries
   - Implement pagination for batches

4. **UX**
   - Dark mode toggle
   - User preferences
   - Batch search/filter
   - Batch export to CSV
   - Multi-language support

### Deployment Checklist

- [ ] Change `SECRET_KEY` in backend .env
- [ ] Update `CORS_ORIGINS` to production domain
- [ ] Change `DATABASE_URL` to production database
- [ ] Update `REACT_APP_API_URL` to production backend
- [ ] Set `RELOAD=False` in backend
- [ ] Build frontend: `npm run build`
- [ ] Use production server (nginx/Apache for frontend, Gunicorn for backend)
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Monitor error logs

### Code Standards

**Frontend:**
- Use functional components with hooks
- Use React Context for state management
- Tailwind CSS for styling
- Components in separate files
- Export default for single export

**Backend:**
- Use FastAPI decorators
- Use Pydantic for validation
- Separate routes, controllers, models
- Type hints for functions
- Proper error handling

---

**Questions?** Check QUICK_START.md or README_FEATURES.md
