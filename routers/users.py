from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from artferia.database import get_session
from artferia.models import User
from artferia.schemas import UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='username already registered'
        )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user



# @router.get('/{user_id}', response_model=UserPublic)
# def read_user(user_id: int, session: Session):
#     """view only one user, by his id"""
#     db_user = session.scalar(select(User).where(User.id == user_id))

#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User not found')
#     else:
#         return db_user

@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}
