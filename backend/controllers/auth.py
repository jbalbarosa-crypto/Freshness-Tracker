import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserResponse


class AuthController:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=AuthController.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, AuthController.SECRET_KEY, algorithm=AuthController.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify a JWT token and return the payload."""
        try:
            payload = jwt.decode(
                token, AuthController.SECRET_KEY, algorithms=[AuthController.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> tuple[str, UserResponse]:
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user
        user = User(full_name=user_data.full_name, email=user_data.email)
        user.set_password(user_data.password)

        db.add(user)
        db.commit()
        db.refresh(user)

        # Create token
        token = AuthController.create_access_token({"sub": user.id, "email": user.email})

        return token, UserResponse.from_orm(user)

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> tuple[str, UserResponse]:
        """Authenticate a user and return token."""
        user = db.query(User).filter(User.email == email).first()

        if not user or not user.verify_password(password):
            raise ValueError("Invalid email or password")

        # Create token
        token = AuthController.create_access_token({"sub": user.id, "email": user.email})

        return token, UserResponse.from_orm(user)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return db.query(User).filter(User.id == user_id).first()
