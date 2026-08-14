import pytest
import contextlib
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker

from core import Base
from models import User, Follow
from services import network

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

    monkeypatch.setattr(network, "get_session", override_get_session)
    
    session = TestingSession()
    yield session
    session.close()

def test_follow_user_success(db_session):
    user_a = User(username="juanitolector", password="megustaleer")
    user_b = User(username="pepitolibros", password="amitambien")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_a.id, user_b.id)

    assert network.is_following(user_a.id, user_b.id) is True

    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 1

    follow_record = db_session.scalar(select(Follow))
    assert follow_record.follower_id == user_a.id
    assert follow_record.followed_id == user_b.id

def test_follow_user_duplicate_safe(db_session):
    user_a = User(username="elviejocubano", password="esepezmegusta")
    user_b = User(username="asíhablozara", password="nietzschecrazy")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_a.id, user_b.id)
    network.follow_user(user_a.id, user_b.id)

    assert network.is_following(user_a.id, user_b.id) is True

    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 1

def test_follow_user_self_is_ignored(db_session):
    user_a = User(username="lemitofsisifo", password="camusrllypenso")

    db_session.add(user_a)
    db_session.commit()

    network.follow_user(user_a.id, user_a.id)

    assert network.is_following(user_a.id, user_a.id) is False

    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 0

def test_unfollow_user_success(db_session):
    user_a = User(username="lectordecuba778", password="tengo78años")
    user_b = User(username="kafkafan112", password="todotienesuproceso")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_a.id, user_b.id)

    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 1

    network.unfollow_user(user_a.id, user_b.id)

    assert network.is_following(user_a.id, user_b.id) is False
    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 0

def test_unfollow_user_not_following(db_session):
    user_a = User(username="leehermano1", password="meencantaleer")
    user_b = User(username="hermanalee2", password="amitambien")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.unfollow_user(user_a.id, user_b.id)

    assert network.is_following(user_a.id, user_b.id) is False
    rows = db_session.scalar(select(func.count()).select_from(Follow))
    assert rows == 0

def test_is_following_directionally(db_session):
    user_a = User(username="fan_cervantes_67", password="novelasejemplaresgoat")
    user_b = User(username="gongora_991", password="narigonthebest")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_a.id, user_b.id)

    assert network.is_following(user_a.id, user_b.id) is True
    assert network.is_following(user_b.id, user_a.id) is False

def test_are_mutual_friends_true(db_session):
    user_a = User(username="don_quijote_lm", password="imnotcrazy")
    user_b = User(username="sancho_panza._.", password="heforsureis")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_a.id, user_b.id)
    network.follow_user(user_b.id, user_a.id)

    assert network.are_mutual_friends(user_a.id, user_b.id) is True
    assert network.are_mutual_friends(user_b.id, user_a.id) is True

def test_are_mutual_friends_false(db_session):
    user_a = User(username="_.harrypotter._", password="griffindorishome")
    user_b = User(username="voldemort_official", password="iwannakillhim")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_b.id, user_a.id)

    assert network.are_mutual_friends(user_a.id, user_b.id) is False

def test_are_mutual_friends_invalid_user(db_session):
    user_a = User(username="dostoievski_fan_xX", password="castigadoporcrimen")

    db_session.add(user_a)
    db_session.commit()

    assert network.are_mutual_friends(user_a.id, (user_a.id+1)) is False

def test_get_followed_and_follower_count(db_session):
    user_a = User(username="sherlokholmes_91", password="iamadetective")
    user_b = User(username="agathacristie", password="iamnotscared")

    db_session.add(user_a)
    db_session.add(user_b)
    db_session.commit()

    network.follow_user(user_b.id, user_a.id)

    assert network.get_follower_count(user_a.id) == 1
    assert network.get_followed_count(user_a.id) == 0
    assert network.get_followed_count(user_b.id) == 1
    assert network.get_follower_count(user_b.id) == 0