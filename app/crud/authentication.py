from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.common.code_generator import generate_code
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(
        fullname=user_data.fullname,
        phone_number=user_data.phone_number,
        password_hash=hashed_password,
        tg_id=user_data.tg_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_phone(db: Session, phone_number: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return None
    return user

def get_user_tg_id(db: Session, tg_id: str):
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        return None
    return user

def get_verification_code(db: Session, user):
    return db.query(VerificationCode).filter(VerificationCode.user_id == user.id).first()

def create_verification_code(db: Session, phone_number: str):
    user = get_user_by_phone(db, phone_number)
    if not user:
        return None
    while True:
        user_expired_codes = get_verification_code(db, user)
        if not user_expired_codes:
            break
        db.delete(user_expired_codes)
        db.commit()
    code = generate_code()
    db_code = VerificationCode(user_id=user.id, code=code)
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

def verify_sent_code(db: Session, user, code: int):
    db_code = get_verification_code(db, user)
    if not db_code:
        raise HTTPException(status_code=404, detail="Code not found")
    if db_code.code != code:
        db_code.attempts += 1
        db.commit()
        if db_code.attempts >= 4:
            db.delete(db_code)
            db.commit()
            raise HTTPException(status_code=400, detail="Too many attempts")
        raise HTTPException(status_code=400, detail="Invalid code")
    if db_code.expires_at < datetime.now():
        db.delete(db_code)
        db.commit()
        raise HTTPException(status_code=400, detail="Code expired")
    db_code.is_used = True
    db.commit()
    return {"status": "success", "message": "Code verified successfully", "code_id": db_code.id}


def delete_verification_code(db: Session, code_id: int):
    db_code = db.query(VerificationCode).get(code_id)
    if not db_code:
        raise HTTPException(status_code=404, detail="Code not found")
    db.delete(db_code)
    db.commit()
    return {"status": "success", "message": "Code deleted successfully"}


def change_password(db: Session, user, new_password: str):
    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return {"status": "success", "message": "Password changed successfully"}


def authenticate_user(phone_number, password, db):
    user = get_user_by_phone(db, phone_number)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user