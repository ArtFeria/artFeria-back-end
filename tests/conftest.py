import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from artferia.app import app
from artferia.models import Base


@pytest.fixture
def client():
    return TestClient(app)


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
