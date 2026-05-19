from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

from app.schemas.user import UserCreate, UserLogin

from app.core.logging_config import logger

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

    logger.info(f"New user registered: {user.email}")

    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        logger.warning(f"Failed login attempt: {user.email}")

        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    logger.info(f"User logged in: {user.email}")

    return {"access_token": token}

