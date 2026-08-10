from sqlalchemy.orm import Session

from models.user import User
from utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.Email == email
    ).first()


def create_user(db: Session, name: str, email: str, password: str):

    hashed_password = hash_password(password)

    new_user = User(
        Name=name,
        Email=email,
        Password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    # -------- TEMPORARY DEBUG --------
    print("=" * 50)
    print("Email:", email)
    print("Entered Password:", password)
    print("Entered Password Length:", len(password))
    print("Stored Password:", user.Password)
    print("Stored Password Length:", len(user.Password))
    print("=" * 50)
    # -------------------------------

    if not verify_password(password, user.Password):
        return None

    return user


def login_user(db: Session, email: str, password: str):

    user = authenticate_user(
        db=db,
        email=email,
        password=password
    )

    if not user:
        return None

    access_token = create_access_token(
        data={
            "sub": str(user.UserID)
        }
    )

    return {
        "message": "Login successful",
        "user_id": user.UserID,
        "access_token": access_token,
        "token_type": "bearer"
    }