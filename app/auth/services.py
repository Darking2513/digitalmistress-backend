from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.auth.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    """CRUD operations for User entity"""
    @staticmethod
    def create(db: Session, user_create: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_create.password)
        db_user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user_id: str, update_data: dict) -> User | None:
        """
        Update allowed fields of a user.
        Prevent mass-assignment of sensitive fields (is_admin, hashed_password, subscription_status)
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        blocked_fields = {"is_admin", "hashed_password", "subscription_status"}
        for key, value in update_data.items():
            if key not in blocked_fields and hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        """
        Delete a user. Ensure the user exists and action is authorized.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True