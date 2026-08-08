from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from core import get_session
from models import Book, UserBook, BookState

def add_book(user_id: int, book: Book, state: BookState) -> None:
    with get_session() as session:
        
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
        else:
            user_book = UserBook(user_id=user_id, book_id=book.id, state=state)
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

def get_user_shelf(user_id: int) -> list[UserBook]:
    with get_session() as session:
        stmt = (
            select(UserBook)
            .options(joinedload(UserBook.book))
            .where(UserBook.user_id == user_id)
        )
        return list(session.scalars(stmt).all())

if __name__ == "__main__":
    from services import search_books
    book = search_books(query='1984 George Orwell')[0]

    add_book(user_id=1, book=book, state=BookState.READ)
    print(f"Successfully added {book} to angel's library.")

    user_shelf = get_user_shelf(user_id=1)
    for user_book in user_shelf:
        print("User book: ", user_book)