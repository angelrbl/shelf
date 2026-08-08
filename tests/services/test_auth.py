import pytest
import contextlib
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from core import Base
from models import User
from services import auth

@pytest.fixture
def db_session(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)

    @contextlib.contextmanager
    def override_get_session():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(auth, "get_session", override_get_session)
    
    session = TestingSession()
    yield session
    session.close()

def test_register_new_user(db_session):
    user = auth.register_user(username="camusfan67", password="iamastranger")

    assert user is not None
    assert user.id is not None
    assert user.username == "camusfan67"
    assert user.check_password("iamastranger") is True

    stmt = select(User).where(User.username == "camusfan67")
    db_user = db_session.scalars(stmt).first()

    assert db_user is not None
    assert db_user.username == "camusfan67"
    assert db_user.check_password("iamastranger") is True

def test_register_existing_user(db_session):
    auth.register_user(username="georgeorwell123", password="1984julia")

    with pytest.raises(ValueError):
        auth.register_user(username="georgeorwell123", password="1984winston")

def test_authenticate_success(db_session):
    auth.register_user(username="samsagregory", password="kafkawasnotcrazy")

    logged_user = auth.authenticate_user(username="samsagregory", password="kafkawasnotcrazy")

    assert logged_user is not None
    assert logged_user.username == "samsagregory"

    stmt = select(User).where(User.username == "samsagregory")
    db_user = db_session.scalars(stmt).first()

    assert db_user is not None
    assert db_user.username == logged_user.username
    
def test_authenticate_failures(db_session):
    auth.register_user(username="lee_bro1", password="leeismybro")

    with pytest.raises(ValueError):
        auth.authenticate_user(username="lee_bro2", password="leeisalsomybro")

    with pytest.raises(ValueError):
        auth.authenticate_user(username="lee_bro1", password="ihavenobrothers")

def test_delete_user_success(db_session):
    user = auth.register_user(username="andy_weir_999", password="hail_mary_for_the_win")
    assert db_session.get(User, user.id) is not None

    auth.delete_user(user_id=user.id, password="hail_mary_for_the_win")
    assert db_session.get(User, user.id) is None

def test_delete_user_does_not_exist(db_session):
    user = auth.register_user(username="xX_lee_Xx", password="iamthereallee")

    with pytest.raises(ValueError):
        auth.delete_user(user_id=(user.id+1), password="iamthereallee")

def test_delete_user_wrong_password(db_session):
    user = auth.register_user(username="Xx_LEE_xX", password="heisnotthereallee")
    
    with pytest.raises(ValueError):
        auth.delete_user(user_id=user.id, password="onlyiamlee")