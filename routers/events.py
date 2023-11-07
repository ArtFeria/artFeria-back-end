from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from artferia.database import get_session
from artferia.models import Event, User
from artferia.schemas import EventSchema, Message
from artferia.security import get_current_user

router = APIRouter(prefix='/events', tags=['events'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=Message)
def read_router():
    return {'detail': 'hello events!'}


@router.post('/', status_code=201, response_model=EventSchema)
def create_event(
    event: EventSchema, session: Session, current_user: CurrentUser
):
    """create one event"""
    has_event = session.scalar(select(Event).where(Event.name == event.name))
    if has_event:
        raise HTTPException(status_code=401, detail='event already exists')

    db_event = Event(
        name=event.name,
        age=event.age,
        description=event.description,
        user_id=current_user.id,
    )

    session.add(db_event)
    session.commit()
    return event
