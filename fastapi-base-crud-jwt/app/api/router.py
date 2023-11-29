from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps, utils
from app.api.schemas import UserCreate, UserUpdate, Token, TokenData
from app.crud.user import create_user, get_user_by_email, update_user
from app.db.session import Session as db_session

router = APIRouter()


@router.post("/signup", response_model=Token)
async def signup(
        user_in: UserCreate,
        db: Session = db_session,
) -> Token:
    db_user = get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user_in=user_in)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        user: TokenData = Depends(deps.get_current_user),
        db: Session = db_session,
) -> Token:
    access_token = utils.create_access_token(
        data={"sub": user.email, "user": {"email": user.email, "username": user.username}})
    refresh_token = utils.create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token,
            "user": {"email": user.email, "username": user.username}, "exp": user.exp, "iat": user.iat}


@router.put("/users/me", response_model=UserUpdate)
async def update_user_me(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: deps.TokenData = Depends(deps.get_current_user),
) -> UserUpdate:
    return update_user(db, user_update, current_user.email)
