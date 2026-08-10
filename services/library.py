from datetime import date
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from core import get_session
from models import Book, UserBook, BookState

def add_book(
        user_id: int,
        book: Book,
        state: BookState = BookState.WISHED,
        start_date: date | None = None,
        end_date: date | None = None,
        rating: int | None = None,
        note: str | None = None
) -> None:
    with get_session() as session:
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("End date must be older than starting date.")
        
        if book.id is None:
            stmt = select(Book).where(Book.google_book_id == book.google_book_id)
            existing_book = session.scalars(stmt).first()

            if existing_book:
                book = existing_book
            else:
                session.add(book)
                session.flush()

        stmt_exist_link = select(UserBook).where(
            UserBook.user_id == user_id, 
            UserBook.book_id == book.id
        )
        existing_link = session.scalars(stmt_exist_link).first()
        if existing_link:
            update_user_book(
                user_id=user_id,
                book_id=book.id,
                state=state,
                start_date=start_date,
                end_date=end_date,
                rating=rating,
                note=note
            )
        else:
            user_book = UserBook(
                user_id=user_id,
                book_id=book.id,
                state=state,
                start_date=start_date,
                end_date=end_date,
                rating=rating,
                note=note
            )
            session.add(user_book)
        session.commit()

def remove_book(user_id: int, book_id: int) -> None:
    with get_session() as session:
        stmt = (
            delete(UserBook)
            .where(UserBook.user_id == user_id, UserBook.book_id == book_id)
        )
        session.execute(stmt)
        session.commit()

def update_book_state(user_id: int, book_id: int, new_state: BookState) -> None:
    with get_session() as session:
        stmt = (
            update(UserBook)
            .where(UserBook.user_id == user_id, UserBook.book_id == book_id)
            .values(state=new_state)
        )
        session.execute(stmt)
        session.commit()

def update_user_book(
        user_id: int,
        book_id: Book,
        state: BookState,
        start_date: date | None = None,
        end_date: date | None = None,
        rating: int | None = None,
        note: str | None = None
) -> None:
    with get_session() as session:
        stmt = (
            update(UserBook)
            .where(UserBook.user_id == user_id, UserBook.book_id == book_id)
            .values(state=state, start_date=start_date, end_date=end_date, rating=rating, note=note)
        )
        session.execute(stmt)
        session.commit()

def get_user_shelf(user_id: int) -> list[UserBook]:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .options(joinedload(UserBook.book))
            .where(UserBook.user_id == user_id)
        )
        return list(session.scalars(stmt).all())

def get_user_book_by_google_id(user_id: int, google_book_id: str) -> None:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .join(UserBook.book)
            .options(joinedload(UserBook.book))
            .where(
                UserBook.user_id == user_id,
                Book.google_book_id == google_book_id
            )
        )
        return session.scalars(stmt).first()