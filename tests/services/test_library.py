import pytest
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base
from models.models import User, BookState
from services import library

BOOK_DATA = {
    "google_book_id": "ABCDEF123456",
    "title": "1984",
    "author": "George Orwell",
    "cover_url": None,
    "description": "A distopic end to the world, leadered by the party",
    "genres": "fiction, dystopia",
    "page_count": "311"
}

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

    monkeypatch.setattr(library, "get_session", override_get_session)
    
    session = TestingSession()
    yield session
    session.close()

def test_add_new_book(db_session):
    user = User(username="anormalbookreader", password="ilovelee")
    db_session.add(user)
    db_session.commit()

    library.add_book(user_id=user.id, book_data=BOOK_DATA, state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert len(user_shelf) == 1
    assert user_shelf[0].book.title == "1984"
    assert user_shelf[0].state == BookState.READ

#TODO: add more tests