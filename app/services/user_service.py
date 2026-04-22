from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserRegisterRequest


class EmailAlreadyRegisteredError(Exception):
    pass


class UsernameTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def create_user(db: Session, payload: UserRegisterRequest) -> User:
    if db.query(User).filter(User.email == payload.email).first():
        raise EmailAlreadyRegisteredError
    if db.query(User).filter(User.username == payload.username).first():
        raise UsernameTakenError

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, str(user.hashed_password)):
        raise InvalidCredentialsError
    return user
