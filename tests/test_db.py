from sqlalchemy import select

from artferia.models import Event, User


def test_db_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_db_create_event(session, user):
    new_event = Event(
        name='rock show',
        age=16,
        description='best rock show ever!',
        user_id=user.id,
    )

    session.add(new_event)
    session.commit()

    event = session.scalar(select(Event).where(Event.user_id == user.id))

    assert event.name == 'rock show'
    assert event.description == 'best rock show ever!'
