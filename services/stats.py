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