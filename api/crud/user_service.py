from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.model import user_model
from api.schema import user_schema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    
def update_user(db: Session, user: user_schema.UserUpdate, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db_user.email = user.email if user.email else db_user.email
        db_user.username = user.username if user.username else db_user.username
        db_user.hashed_password = pwd_context.hash(user.password) if user.password else db_user.hashed_password
        

        db.commit()
        db.refresh(db_user)
        return db_user
       