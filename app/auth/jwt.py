from datetime import datetime, timedelta, timezone

from jose import jwt

from config.settings import settings


def create_access_token(
    data: dict,
) -> str:

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire,
    })

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )