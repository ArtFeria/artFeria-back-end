from typing import Annotated
from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from artferia.models import Event
from artferia.schemas import EventSchema, Message
from artferia.database import get_session
from artferia.security import get_current_user

router = APIRouter(prefix='/events', tags=['events'])

Session = Annotated[Session, Depends(get_session)]

@router.get('/', response_model=Message)
def read_events():
    return {'detail': 'hello events!'}


@router.post('/', response_model=EventSchema)
def create_event(event: EventSchema, session: Session):
    """create one event"""

    session.add(event)
    session.commit()
    session.refresh(event)
    return event
