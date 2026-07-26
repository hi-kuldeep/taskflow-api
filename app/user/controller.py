from datetime import timedelta
from app.user.dto.login_dto import LoginResponse, LoginSchema
from fastapi import status
from app.constant.exception import CustomException
from app.user.models import UserModel
from sqlalchemy.orm import Session
from app.user.dto.user_dto import UserResponseSchema, UserSchema
from app.core.config import settings
from app.utils.security import get_password_hash, verify_password, create_access_token


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


def login_user(user: LoginSchema, db: Session) -> LoginResponse:

    is_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not is_user:
        raise CustomException("User not found", status_code=status.HTTP_404_NOT_FOUND)

    hashed_password = str(is_user.password)

    if not verify_password(user.password, hashed_password):
        raise CustomException(
            "Invalid password", status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(
        user=UserResponseSchema.model_validate(is_user), token=access_token
    )
