from fastapi import APIRouter

from artferia.schemas import UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    return user
