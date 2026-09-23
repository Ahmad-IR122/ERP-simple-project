import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from svix.webhooks import Webhook, WebhookVerificationError

from app.core.config import settings
from app.core.database import get_db
from app.modules.users.models import User

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post("/clerk")
async def clerk_webhook(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    payload = await request.body()

    headers = {
        "svix-id": request.headers.get("svix-id"),
        "svix-timestamp": request.headers.get("svix-timestamp"),
        "svix-signature": request.headers.get("svix-signature"),
    }

    if not all(headers.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing webhook headers",
        )

    webhook = Webhook(settings.CLERK_WEBHOOK_SECRET)

    try:
        webhook.verify(
            payload,
            headers,
        )
    except WebhookVerificationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature",
        ) from exc

    try:
        event = json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook payload",
        ) from exc

    event_type = event.get("type")
    data = event.get("data", {})

    print("CLERK EVENT:", event_type)

    if event_type == "user.created":
        clerk_user_id = data.get("id")

        email_addresses = data.get("email_addresses", [])
        primary_email_id = data.get("primary_email_address_id")

        email = None

        for item in email_addresses:
            if item.get("id") == primary_email_id:
                email = item.get("email_address")
                break

        if not email and email_addresses:
            email = email_addresses[0].get("email_address")

        existing_user = (
            db.query(User)
            .filter(User.clerk_user_id == clerk_user_id)
            .first()
        )

        if not existing_user:
            user = User(
                clerk_user_id=clerk_user_id,
                email=email,
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                role="employee",
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            print("USER CREATED:", clerk_user_id)

    elif event_type == "user.updated":
        clerk_user_id = data.get("id")

        user = (
            db.query(User)
            .filter(User.clerk_user_id == clerk_user_id)
            .first()
        )

        if user:
            email_addresses = data.get("email_addresses", [])
            primary_email_id = data.get("primary_email_address_id")

            email = None

            for item in email_addresses:
                if item.get("id") == primary_email_id:
                    email = item.get("email_address")
                    break

            if not email and email_addresses:
                email = email_addresses[0].get("email_address")

            user.email = email
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")

            db.commit()

            print("USER UPDATED:", clerk_user_id)

    elif event_type == "user.deleted":
        clerk_user_id = data.get("id")

        user = (
            db.query(User)
            .filter(User.clerk_user_id == clerk_user_id)
            .first()
        )

        if user:
            db.delete(user)
            db.commit()

            print("USER DELETED:", clerk_user_id)

    return {
        "status": "ok",
        "event": event_type,
    }