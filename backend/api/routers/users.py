from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserResponse, UserUpdate
from controllers.auth import AuthController

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user(
    authorization: str = Header(None), db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = AuthController.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = AuthController.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
def update_me(
    updates: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user information."""
    if updates.full_name:
        current_user.full_name = updates.full_name
    if updates.email:
        current_user.email = updates.email

    db.commit()
    db.refresh(current_user)
    return UserResponse.from_orm(current_user)
