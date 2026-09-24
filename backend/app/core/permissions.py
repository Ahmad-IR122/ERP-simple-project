from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.auth import get_current_user
from app.modules.users.models import User

def require_role(required_role: str) -> Callable:
  def role_checker(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != required_role:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
      )
    return current_user
  return role_checker