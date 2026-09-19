from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class DuplicateUserError(Exception):
    pass


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at, User.id)))


def get_user(db: Session, user_id: UUID) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise UserNotFoundError
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateUserError from exc
    db.refresh(user)
    return user


def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
    user = get_user(db, user_id)
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateUserError from exc
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: UUID) -> None:
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
