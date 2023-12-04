import factory
from factory import fuzzy
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from artferia.app import app
from artferia.database import get_session
from artferia.models import Base, Event, User
from artferia.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    yield Session()

    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'senhateste'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def other_user(session):
    password = 'senhateste231'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def event(session):
    event = EventFactory()

    session.add(event)
    session.commit()
    session.refresh()
    return event


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda obj: f'test{obj.id}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)
    
    fuz = fuzzy.FuzzyInteger(21)
    fake = Faker(['en_US', 'pt_BR'])

    id = factory.sequence(lambda n: n)
    name = factory.Faker('name')
    age = fuz.fuzz()
    description = fake.address()
    location = None
    organizer = user.id   # user_id
