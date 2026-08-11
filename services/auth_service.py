from sqlalchemy.orm import Session

from models.user import User
from models.role import Role

from utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.Email == email
    ).first()


def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(
        Role.RoleName == role_name
    ).first()


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    hashed_password = hash_password(password)

    member_role = get_role_by_name(
        db,
        "Member"
    )

    new_user = User(
        Name=name,
        Email=email,
        Password=hashed_password,
        RoleID=member_role.RoleID if member_role else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.Password
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = authenticate_user(
        db=db,
        email=email,
        password=password
    )

    if not user:
        return None

    access_token = create_access_token(
        data={
            "sub": str(user.UserID),
            "role_id": user.RoleID
        }
    )

    return {
        "message": "Login successful",
        "user_id": user.UserID,
        "access_token": access_token,
        "token_type": "bearer"
    }