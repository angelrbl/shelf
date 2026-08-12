from services.catalog import search_books
from services.library import add_book, update_book_state, update_user_book, remove_book, get_user_shelf, filter_user_shelf, get_unique_shelf_genres, get_user_book_by_google_id
from services.auth import register_user, authenticate_user, delete_user, get_user_by_id
from services.stats import total_read_books, average_book_rating, total_read_books_this_year

__all__ = [
    "search_books",
    "add_book",
    "update_book_state",
    "update_user_book",
    "remove_book",
    "get_user_shelf",
    "filter_user_shelf",
    "get_unique_shelf_genres",
    "get_user_book_by_google_id",
    "register_user",
    "authenticate_user",
    "delete_user",
    "get_user_by_id",
    "total_read_books",
    "average_book_rating",
    "total_read_books_this_year"
]