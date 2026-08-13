from fastapi import HTTPException, status

from app.core.config import get_settings


def validate_user_message(message: str) -> str:
    settings = get_settings()
    cleaned = message.strip()

    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty.",
        )

    if len(cleaned) > settings.max_input_chars:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Message exceeds the configured input limit.",
        )

    return cleaned


def public_safe_error_message() -> str:
    return "The request could not be processed. Please try again."
