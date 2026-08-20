from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.role import Role


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

print("SECRET KEY LENGTH:", len(SECRET_KEY))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env file")


# --------------------------------------------------
# JWT SETTINGS
# --------------------------------------------------

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


# --------------------------------------------------
# PASSWORD HASHING
# --------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# --------------------------------------------------
# JWT BEARER AUTHENTICATION
# --------------------------------------------------

bearer_scheme = HTTPBearer()


# --------------------------------------------------
# PASSWORD FUNCTIONS
# --------------------------------------------------

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# --------------------------------------------------
# CREATE ACCESS TOKEN
# --------------------------------------------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --------------------------------------------------
# GET CURRENT USER
# --------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):

    token = credentials.credentials

    print("TOKEN RECEIVED:", token[:20])

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("JWT PAYLOAD:", payload)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user_id

    except JWTError as e:

        print("JWT ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user_id

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# --------------------------------------------------
# SYSTEM ADMIN AUTHORIZATION
# --------------------------------------------------

def require_system_admin(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.UserID == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    system_admin_role = db.query(Role).filter(
        Role.RoleName == "System Admin"
    ).first()

    if not system_admin_role:
        raise HTTPException(
            status_code=500,
            detail="System Admin role not found"
        )

    if user.RoleID != system_admin_role.RoleID:
        raise HTTPException(
            status_code=403,
            detail="System Admin access required"
        )

    return system_admin_role.RoleID