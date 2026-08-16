import pytest
import contextlib
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import Base
from models import User, BookState, Book
from services import library

def get_sample_book():
    return Book(
        google_book_id = "ABCDEF123456",
        title = "1984",
        author = "George Orwell",
        cover_url = None,
        description = "A distopic end to the world, leadered by the party",
        genres = "fiction, dystopia",
        page_count = "311"
    )

def get_another_sample_book():
    return Book(
        google_book_id = "123456ABCDEF",
        title = "El Extranjero",
        author = "Albert Camus",
        cover_url = None,
        description = "An indifferent man judged for his world vision",
        genres = "fiction, philosphy",
        page_count = "120"
    )

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

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert len(user_shelf) == 1
    assert user_shelf[0].book.title == "1984"
    assert user_shelf[0].state == BookState.READ

def test_add_existing_book_updates_book(db_session):
    user = User(username="thebooksreadme", password="ialsolovelee")
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.WISHED, rating=7, start_date=date(2007, 5, 19), end_date=date(2026, 5, 19))

    same_book = get_sample_book()
    library.add_book(user_id=user.id, book=same_book, state=BookState.READ, rating=9, end_date=date(2026, 8, 12))

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert len(user_shelf) == 1
    assert user_shelf[0].state == BookState.READ
    assert user_shelf[0].end_date == date(2026, 8, 12)
    assert user_shelf[0].rating == 9

def test_add_book_already_in_db(db_session):
    user = User(username="beenreadinallday", password="irllyrllylovelee")
    existing_book = get_sample_book()

    db_session.add(user)
    db_session.add(existing_book)
    db_session.commit()

    library.add_book(user_id=user.id, book=existing_book, state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert len(user_shelf) == 1
    assert user_shelf[0].book_id == existing_book.id

def test_add_book_wrong_date_order(db_session):
    user = User(username="omgilovereadingsm", password="iwishicouldbelee")

    db_session.add(user)
    db_session.commit()

    book = get_sample_book()

    with pytest.raises(ValueError):
        library.add_book(user_id=user.id, book=book, start_date=date(2026, 8, 12), end_date=date(2026, 5, 19))

def test_update_book_state(db_session):
    user = User(username="imaworm", password="leeisthebest")
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.WISHED)

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[0].book_id

    library.update_book_state(user_id=user.id, book_id=book_id, new_state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert user_shelf[0].state == BookState.READ

def test_remove_book(db_session):
    user = User(username="wormandwarm", password="wassuplee")
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.WISHED)

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[0].book_id

    library.remove_book(user_id=user.id, book_id=book_id)

    user_shelf = library.get_user_shelf(user_id=user.id)
    assert len(user_shelf) == 0

def test_get_currently_reading_book(db_session):
    user = User(username="therealbookgoat", password="iswearleeistop")
    db_session.add(user)
    db_session.commit()

    assert library.get_currently_reading_books(user_id=user.id) is None

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, start_date=date(2026, 5, 19))
    assert library.get_currently_reading_books(user_id=user.id) is None

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[0].book_id
    library.update_book_state(user_id=user.id, book_id=book_id, new_state=BookState.READING)
    assert library.get_currently_reading_books(user_id=user.id) is not None
    assert library.get_currently_reading_books(user_id=user.id).book_id == book_id

    another_book = get_another_sample_book()
    library.add_book(user_id=user.id, book=another_book, state=BookState.READ, start_date=date(2026, 4, 19))
    assert library.get_currently_reading_books(user_id=user.id).book_id == book_id

def test_get_user_book(db_session):
    user = User(username="santiposteguillo345", password="itsmelee")
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[0].book_id

    assert library.get_user_book(user_id=user.id, book_id=book_id) is not None
    assert library.get_user_book(user_id=user.id, book_id=book_id).book_id == book_id
    assert library.get_user_book(user_id=user.id, book_id=(book_id + 1)) is None

def test_get_user_book_by_google_id(db_session):
    user = User(username="mysoulisreading", password="leewssupgng")
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    google_id = book.google_book_id
    library.add_book(user_id=user.id, book=book, state=BookState.READ)

    user_shelf = library.get_user_shelf(user_id=user.id)
    user_book_by_google_id = library.get_user_book_by_google_id(user_id=user.id, google_book_id=google_id)

    another_user_book_by_google_id = library.get_user_book_by_google_id(user_id=user.id, google_book_id="ABCDEFGHIJKLM")

    assert user_shelf[0].book_id == user_book_by_google_id.book_id
    assert another_user_book_by_google_id is None