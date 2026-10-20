from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.models.business_profile import BusinessProfile
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.core.audit_logger import log_audit_event
import uuid

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user = User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role or "taxpayer",
        is_verified=True
    )
    db.add(user)
    db.flush()

    # Create default business profile
    profile = BusinessProfile(
        id=str(uuid.uuid4()),
        user_id=user.id,
        profession="Software Developer",
        business_type="Freelance/Self-Employed",
        country="India",
        jurisdiction="Income Tax Department (CBDT)",
        tax_year="2024-2025",
        tax_regime="Sec 44ADA (Presumptive)"
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    log_audit_event(db, user.id, "USER_SIGNUP", "User", user.id)

    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = create_access_token(user.id)
    log_audit_event(db, user.id, "USER_LOGIN", "User", user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(user_id: str = "demo-user-1", db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found. Please seed database.")
    return user
