from datetime import date
from sqlalchemy import func, select, update, delete
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
) -> UserBook:
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
            existing_link.state = state
            existing_link.start_date = start_date
            existing_link.end_date = end_date
            existing_link.rating = rating
            existing_link.note = note

            user_book = existing_link
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

        session.refresh(user_book)
        return user_book

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

def update_top_shelf_rank(user_id: int, book_id: int, new_top_shelf_rank: int | None) -> None:
    with get_session() as session:
        stmt = (
            update(UserBook)
            .where(UserBook.user_id == user_id,
                   UserBook.book_id == book_id
            )
            .values(top_shelf_rank=new_top_shelf_rank)
        )
        session.execute(stmt)
        session.commit()

def toggle_most_wished(user_id: int, book_id: int, status: bool, max_limit: int = 5) -> None:
    with get_session() as session:
        if status is True:
            stmt = select(func.count()).where(
                UserBook.user_id == user_id, 
                UserBook.is_most_wished == True
            )
            most_wished_count = session.execute(stmt).scalar()
            
            if most_wished_count >= max_limit:
                raise ValueError(f"You can only have up to {max_limit} books in Most Wished.")
            
        stmt = (
            update(UserBook)
            .where(UserBook.user_id == user_id,
                   UserBook.book_id == book_id
            )
            .values(is_most_wished=status)
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

def filter_user_shelf(shelf: list[UserBook], query: str | None = None, state: BookState | None = None, genre: str | None = None) -> list[UserBook]:
    filtered_books = []

    words = query.strip().lower().split() if query else []
    target_genre = genre.strip().lower() if genre else None

    for user_book in shelf:
        title = user_book.book.title.lower()
        author = user_book.book.author.lower()

        matches_text = all(word in title or word in author for word in words)
        
        matches_state = (state is None) or (user_book.state == state)
        matches_genre = True
        if target_genre:
            if user_book.book.genres:
                book_genres = [g.strip().lower() for g in user_book.book.genres.split(',')]
                matches_genre = target_genre in book_genres
            else:
                matches_genre = False

        if matches_text and matches_state and matches_genre:
            filtered_books.append(user_book)

    return filtered_books

def get_unique_shelf_genres(shelf: list[UserBook]) -> list[str]:
    unique_genres = set()

    for user_book in shelf:
        if user_book.book.genres:
            genres = user_book.book.genres.split(',')
            for g in genres:
                clean_genre = g.strip().title()
                if clean_genre:
                    unique_genres.add(clean_genre)

    return sorted(list(unique_genres))

def get_currently_reading_books(user_id: int, max_results: int = 3) -> list[UserBook] | None:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .where(
                UserBook.user_id == user_id,
                UserBook.state == BookState.READING
            )
            .order_by(UserBook.start_date.desc())
            .options(joinedload(UserBook.book))
            .limit(max_results)
        )
        return list(session.scalars(stmt).all())

def get_top_shelf(user_id: int) -> list[UserBook]:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .where(
                UserBook.user_id == user_id,
                UserBook.top_shelf_rank.isnot(None)
            )
            .options(joinedload(UserBook.book))
        )
        return list(session.scalars(stmt).all()) or []
    
def get_most_wished(user_id: int, max_results: int = 5) -> list[UserBook]:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .where(
                UserBook.user_id == user_id,
                UserBook.is_most_wished == True
            )
            .options(joinedload(UserBook.book))
            .limit(max_results)
        )
        return list(session.scalars(stmt).all()) or []

def get_user_book(user_id: int, book_id: int) -> UserBook | None:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .options(joinedload(UserBook.book))
            .where(UserBook.user_id == user_id, UserBook.book_id == book_id)
        )
        return session.scalars(stmt).first()

def get_user_book_by_google_id(user_id: int, google_book_id: str) -> UserBook| None:
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

if __name__ == "__main__":
    from services import search_books
    book = search_books(query='1984 George Orwell')[0]

    add_book(user_id=1, book=book, state=BookState.READ)
    print(f"Successfully added {book} to angel's library.")

    user_shelf = get_user_shelf(user_id=1)
    for user_book in user_shelf:
        print("User book: ", user_book)