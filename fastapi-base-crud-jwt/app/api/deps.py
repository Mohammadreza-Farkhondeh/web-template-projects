from typing import Optional, Any
import jwt

from fastapi import Header, HTTPException, Depends, status

from app.db.session import Session
from app.core.config import settings


async def verify_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_user_id(authorization: str = Header(None)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = authorization.split("Bearer ")[1]
        payload = await verify_token(token)
        user_id = payload.get("id")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user_id(user_id: str = Depends(get_user_id)):
    return user_id


from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.schemas import Token
from app.crud.user import get_user_by_email
from app.db.session import Session as db_session
from app.api.utils import get_token


def get_current_user(token: str = Depends(get_token), db: Session = db_session) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authentication": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token = Token(**payload)
        email = token.email
        if email is None or get_user_by_email(db, email) is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return token
