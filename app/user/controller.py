from fastapi import status
from app.constant.exception import CustomException
from app.user.models import UserModel
from sqlalchemy.orm import Session
from app.user.dtos import UserSchema
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def create_user(user: UserSchema, db: Session):
    is_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if is_user:
        raise CustomException(
            "User email is already exists", status_code=status.HTTP_400_BAD_REQUEST
        )

    is_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if is_user:
        raise CustomException(
            "User username is already exists", status_code=status.HTTP_400_BAD_REQUEST
        )

    hash_password = get_password_hash(user.password)

    try:
        new_user = UserModel(
            username=user.username, email=user.email, password=hash_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise e
