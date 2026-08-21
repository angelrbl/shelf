from datetime import date, timedelta

from sqlalchemy import select, func, extract, or_

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

def user_books_by_genre(user_id: int) -> dict[str, int]:
    with get_session() as session:
        stmt = (
            select(Book.genres)
            .join(UserBook.book)
            .select_from(UserBook)
            .where(UserBook.user_id == user_id, or_(UserBook.state == BookState.READ, UserBook.state == BookState.DROPPED), Book.genres.is_not(None))
        )

        raw_genres_list = list(session.scalars(stmt).all())

        books_by_genre = {}

        for raw_genre in raw_genres_list:
            for genre in raw_genre.split(','):
                if clean_genre := genre.strip():
                    books_by_genre[clean_genre] = books_by_genre.get(clean_genre, 0) + 1

        return books_by_genre

def get_heatmap_data(user_id: int) -> list[list[(str, int | None)]]:
    with get_session() as session:
        stmt = (
            select(UserBook.start_date, UserBook.end_date, Book.page_count)
            .join(UserBook.book)
            .select_from(UserBook)
            .where(UserBook.user_id == user_id,
                   or_(UserBook.state == BookState.READ, UserBook.state == BookState.DROPPED),
                   UserBook.start_date.is_not(None),
                   UserBook.end_date.is_not(None),
                   Book.page_count.is_not(None)
                )
        )

        read_books = list(session.execute(stmt).all())

        daily_pages = {}

        for start_date, end_date, page_count in read_books:
            days_spent = (end_date - start_date).days + 1

            if days_spent <= 0:
                days_spent = 1

            pages_per_day = page_count // days_spent

            for i in range(days_spent):
                current_date = start_date + timedelta(days=i)
                date_str = current_date.strftime('%Y-%m-%d')

                daily_pages[date_str] = daily_pages.get(date_str, 0) + pages_per_day

        return [[date, pages] for date, pages in daily_pages.items()]
