from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from artferia.database import get_session
from artferia.models import User
from artferia.schemas import Message, UserPublic, UserSchema
from artferia.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    """create one user"""
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='username already registered'
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    """update one user data by his id"""

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='not enough permissions')

    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail='user not found')

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email

    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session):
    """view one user data by his id"""
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='user not found')

    return db_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session):
    """delete one user by his id"""
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='user not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'user deleted'}
