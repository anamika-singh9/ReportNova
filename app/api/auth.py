from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import User

from app.schemas.auth import (
    UserSignup,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from app.auth.password import (
    hash_password,
    verify_password,
)

from app.auth.jwt import create_access_token

from app.auth.dependencies import (
    get_current_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==================================================
# SIGNUP
# ==================================================

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==================================================
# LOGIN
# ==================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    password_valid = verify_password(
        user_data.password,
        user.password_hash,
    )

    if not password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ==================================================
# GET CURRENT USER
# ==================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return current_user