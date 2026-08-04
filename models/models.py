from datetime import date
import hashlib
from typing import Optional
from enum import Enum
from sqlalchemy import String, Text, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core import Base

class BookState(Enum):
    WISHED = "wished"
    READING = "reading"
    READ = "read"
    DROPPED = "dropped"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column()

    user_books: Mapped[list["UserBook"]] = relationship(back_populates="user")

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password):
        self.password_hash = self.hash_password(password)

    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    google_book_id: Mapped[str] = mapped_column(String(50), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(200))
    cover_url: Mapped[Optional[str]] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    genres: Mapped[Optional[str]] = mapped_column(String(200))
    page_count: Mapped[Optional[int]] = mapped_column()

    user_books: Mapped[list["UserBook"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"Book(id={self.id}, google_book_id={self.google_book_id}, title={self.title}, author={self.author})"

class UserBook(Base):
    __tablename__ = "user_book"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    state: Mapped[BookState] = mapped_column(default=BookState.WISHED)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    rating: Mapped[Optional[int]] = mapped_column()
    note: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="user_books")
    book: Mapped[Book] = relationship(back_populates="user_books")

    def __repr__(self):
        return f"UserBook(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, state={self.state})"

    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uix_user_book'),
    )