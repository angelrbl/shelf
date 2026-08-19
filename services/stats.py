from datetime import date

from sqlalchemy import select, func, extract

from core import get_session
from models import Book, UserBook, BookState

def total_read_books(user_id: int) -> int:
    with get_session() as session:
        stmt = (
            select(func.count())
            .select_from(UserBook)
            .where(UserBook.user_id == user_id, UserBook.state == BookState.READ)
        )

        return session.scalar(stmt) or 0

def average_book_rating(user_id: int) -> float:
    with get_session() as session:
        stmt = (
            select(func.avg(UserBook.rating))
            .select_from(UserBook)
            .where(UserBook.user_id == user_id, UserBook.state == BookState.READ)
        )

        return session.scalar(stmt) or 0.0

def total_read_books_this_year(user_id: int) -> int:
    with get_session() as session:
        stmt = (
            select(func.count())
            .select_from(UserBook)
            .where(UserBook.user_id == user_id, UserBook.state == BookState.READ)
            .where(extract("year", UserBook.end_date) == date.today().year)
        )

        return session.scalar(stmt) or 0

def user_books_by_genre(user_id: int):
    with get_session() as session:
        stmt = (
            select(Book.genres)
            .join(UserBook.book)
            .select_from(UserBook)
            .where(UserBook.user_id == user_id, UserBook.state == BookState.READ, Book.genres.is_not(None))
        )

        raw_genres_list = list(session.scalars(stmt).all())

        books_by_genre = {}

        for raw_genre in raw_genres_list:
            for genre in raw_genre.split(','):
                if clean_genre := genre.strip():
                    books_by_genre[clean_genre] = books_by_genre.get(clean_genre, 0) + 1

        return books_by_genre