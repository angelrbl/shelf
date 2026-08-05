import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models import User, Book, UserBook, BookState
from core import Base

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    yield session
    session.close()

def test_user_password_hashing(db_session):
    user = User(username="bookworm123", password="megustanloslibros")
    
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.password_hash != "megustanloslibros"
    assert user.check_password("megustanloslibros")

def test_user_book_relationship(db_session):
    user = User(username="hermanolee1", password="ilovemybro")
    book = Book(google_book_id="IDKIHNC", title="1984", author="George Orwell")

    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    user_book = UserBook(user_id=user.id, book_id=book.id, state=BookState.READING)
    db_session.add(user_book)
    db_session.commit()

    assert len(user.user_books) == 1
    assert user.user_books[0].book_id == book.id

def test_unique_constraint_user_book(db_session):
    user = User(username="hermanolee2", password="ilovemybro")
    book = Book(google_book_id="IDKIDGAF", title="Julia", author="Sandra Newman")

    user_book = UserBook(user=user, book=book)
    db_session.add(user_book)
    db_session.commit()

    user_book_2 = UserBook(user_id=user.id, book_id=book.id)
    db_session.add(user_book_2)

    with pytest.raises(IntegrityError):
        db_session.commit()