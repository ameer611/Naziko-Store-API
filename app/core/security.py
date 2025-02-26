import os
import dotenv
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

dotenv.load_dotenv()

# Hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")

def hash_password(password: str) -> str:
    """Hash the given password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user information from the JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Load secret key and algorithm from environment variables
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    if not SECRET_KEY or not ALGORITHM:
        raise RuntimeError("SECRET_KEY or ALGORITHM is not set in environment variables")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        phone_number: str = payload.get("phone_number")
        is_admin: bool = payload.get("is_admin")
        is_superuser: bool = payload.get("is_superuser")
        if phone_number is None or user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "phone_number": phone_number, "is_admin": is_admin, "is_superuser": is_superuser}
    except JWTError:
        raise credentials_exception
