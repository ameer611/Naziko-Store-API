from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.crud.authentication import create_user, get_user_by_phone, create_verification_code, \
    verify_sent_code, delete_verification_code, change_password, authenticate_user, get_user_tg_id
from app.db.base import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.verification_sent_code import VerificationSentCode
from app.service.telegram import send_code_via_bot

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    This endpoint is used for user registration.
    :param user: UserCreate schema
    :param db: Session
    :return: UserResponse schema
    """
    existing_user = get_user_by_phone(db, user.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    if get_user_tg_id(db, user.tg_id):
        raise HTTPException(status_code=400, detail="Telegram id already registered")
    user = create_user(db, user)
    return user


@router.post("/send-code", response_model=dict, status_code=200)
async def send_code(phone_number: str, db: Session = Depends(get_db)):
    """
    This endpoint is used to send verification code to the user's telegram account.
    :param phone_number:
    :param db:
    :return: message
    """
    user = get_user_by_phone(db, phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user.tg_id)
    if not user.tg_id:
        raise HTTPException(status_code=400, detail="User has no telegram id")
    db_code = create_verification_code(db, phone_number)
    result = send_code_via_bot(user.tg_id, db_code.code)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to send code")
    return {"status": "success", "message": "Code sent successfully"}


@router.post("/verify-code-and-change-password", response_model=dict, status_code=200)
async def verify_code(data: VerificationSentCode, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, data.phone_number)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    code_message = verify_sent_code(db, db_user, data.code)
    if code_message:
        delete_verification_code(db, code_message["code_id"])
    message = change_password(db, db_user, data.new_password)
    if not message:
        raise HTTPException(status_code=500, detail="Failed to change password")
    return message


@router.post("/login", response_model=dict, status_code=200)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    token = create_access_token({"sub": str(user.id),
                                 "phone_number": user.phone_number,
                                 'fullname': str(user.fullname),
                                 "is_admin": user.is_admin,
                                 "is_superuser": user.is_superuser}, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
