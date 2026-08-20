import pytest
import contextlib
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import Base
from models import User, BookState, Book
from services import stats
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
        genres = "fiction, philosophy",
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

    monkeypatch.setattr(stats, "get_session", override_get_session)
    monkeypatch.setattr(library, "get_session", override_get_session)
    
    session = TestingSession()
    yield session
    session.close()

def test_total_books_read(db_session):
    user = User(username="iforgotleeexists", password="icannotbelieveit")

    db_session.add(user)
    db_session.commit()
    assert stats.total_read_books(user_id=user.id) == 0

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.WISHED)
    assert stats.total_read_books(user_id=user.id) == 0

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[0].book_id
    library.update_book_state(user_id=user.id, book_id=book_id, new_state=BookState.READ)
    assert stats.total_read_books(user_id=user.id) == 1

def test_total_books_read_invalid_user(db_session):
    user = User(username="camusdidit", password="ohmylee")
    
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ)

    assert stats.total_read_books(user_id=(user.id + 1)) == 0

def test_average_rating(db_session):
    user = User(username="iforgotleeexists", password="icannotbelieveit")

    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, rating=0)

    assert stats.average_book_rating(user_id=user.id) == 0.0

    another_book = get_another_sample_book()
    library.add_book(user_id=user.id, book=another_book, state=BookState.READ, rating=10)

    assert stats.average_book_rating(user_id=user.id) == 5.0

def test_average_rating_no_ratings(db_session):
    user = User(username="andyweirlovesspace", password="leelaaluu")
    
    db_session.add(user)
    db_session.commit()

    assert stats.average_book_rating(user_id=user.id) == 0.0

def test_total_read_books_this_year(db_session):
    user = User(username="kafkawasabeetle", password="gregorylovedlee")
    
    db_session.add(user)
    db_session.commit()
    assert stats.total_read_books_this_year(user_id=user.id) == 0

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, end_date=date(2025, 5, 19))
    assert stats.total_read_books_this_year(user_id=user.id) == 0

    book = get_another_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.WISHED, end_date=date(2026, 5, 19))
    assert stats.total_read_books_this_year(user_id=user.id) == 0

    user_shelf = library.get_user_shelf(user_id=user.id)
    book_id = user_shelf[1].book_id
    library.update_book_state(user_id=user.id, book_id=book_id, new_state=BookState.READ)
    assert stats.total_read_books_this_year(user_id=user.id) == 1

def test_user_books_by_genre(db_session):
    user = User(username="theoldman", password="ilovethesea")
        
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, end_date=date(2025, 5, 19))

    book = get_another_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, end_date=date(2026, 5, 19))

    print(stats.user_books_by_genre(user_id=user.id))
    assert stats.user_books_by_genre(user_id=user.id) == {'fiction': 2, 'dystopia': 1, 'philosophy': 1}

def test_get_heatmap_data(db_session):
    user = User(username="sisifoooo_xXx", password="cAmUsGoD")
            
    db_session.add(user)
    db_session.commit()

    book = get_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, start_date=date(2026, 5, 18), end_date=date(2026, 5, 19))

    assert stats.get_heatmap_data(user_id=user.id) == [['2026-05-18', 155], ['2026-05-19', 155]]

    book = get_another_sample_book()
    library.add_book(user_id=user.id, book=book, state=BookState.READ, start_date=date(2026, 5, 19), end_date=date(2026, 5, 20))

    assert stats.get_heatmap_data(user_id=user.id) == [['2026-05-18', 155], ['2026-05-19', 215], ['2026-05-20', 60]]