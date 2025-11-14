from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, UserResponse
from controllers.auth import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        token, user = AuthController.register_user(db, request)
        return {"access_token": token, "user": user}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with email and password."""
    try:
        token, user = AuthController.login_user(db, request.email, request.password)
        return {"access_token": token, "user": user}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
