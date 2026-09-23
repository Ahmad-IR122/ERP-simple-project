from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.modules.users.models import User


security = HTTPBearer()

jwk_client = PyJWKClient(settings.CLERK_JWKS_URL)


def verify_clerk_token(token: str) -> dict:
    try:
        unverified_payload = jwt.decode(
            token,
            options={"verify_signature": False},
        )

        print("TOKEN ISSUER:", unverified_payload.get("iss"))
        print("EXPECTED ISSUER:", settings.CLERK_ISSUER_URL)

        signing_key = jwk_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.CLERK_ISSUER_URL,
            options={
                "verify_aud": False,
            },
        )

        print("TOKEN VERIFIED")
        print("USER ID:", payload.get("sub"))

        return payload

    except jwt.ExpiredSignatureError as exc:
        print("TOKEN EXPIRED:", exc)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        ) from exc

    except jwt.InvalidTokenError as exc:
        print(
            "INVALID TOKEN:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    except Exception as exc:
        print(
            "AUTH ERROR:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        ) from exc


def get_current_clerk_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> dict:
    return verify_clerk_token(credentials.credentials)


def get_current_user(
    clerk_user: Annotated[
        dict,
        Depends(get_current_clerk_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> User:
    clerk_user_id = clerk_user.get("sub")

    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Clerk user",
        )

    user = (
        db.query(User)
        .filter(User.clerk_user_id == clerk_user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist in ERP database",
        )

    return user