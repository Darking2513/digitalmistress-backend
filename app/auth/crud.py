from sqlalchemy.orm import Session
from .models import User
from .security import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, email: str, password: str, full_name: str = None) -> User:
    hashed_pw = hash_password(password)
    user = User(email=email, hashed_password=hashed_pw, full_name=full_name)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email already exists")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None