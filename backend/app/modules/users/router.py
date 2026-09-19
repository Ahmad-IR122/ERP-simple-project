from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate
from app.modules.users.service import (
    DuplicateUserError,
    UserNotFoundError,
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)) -> list[UserRead]:  # noqa: B008
    return list_users(db)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserRead:  # noqa: B008
    try:
        return create_user(db, user_data)
    except DuplicateUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this Clerk user ID or email already exists",
        ) from exc


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db)) -> UserRead:  # noqa: B008
    try:
        return get_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc


@router.patch("/{user_id}", response_model=UserRead)
def edit_user(
    user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)  # noqa: B008
) -> UserRead:
    try:
        return update_user(db, user_id, user_data)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    except DuplicateUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this Clerk user ID or email already exists",
        ) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: UUID, db: Session = Depends(get_db)) -> None:  # noqa: B008
    try:
        delete_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
