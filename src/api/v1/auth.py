from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import DBSession, UserServiceDep
from src.core.security import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSession,
    service: UserServiceDep,
):
    # Call the service layer instead of the repo directly
    user = await service.authenticate_user(
        session, username=form_data.username, password=form_data.password
    )

    # 1. Check for inactive user first (400 Bad Request)
    if user and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # 2. Check for invalid credentials (401 Unauthorized)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
