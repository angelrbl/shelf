import requests
from sqlalchemy import select, and_, or_

from models import Book

from core import GOOGLE_BOOKS_API_KEY, get_session

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

def search_books(query: str, max_results: int=5, google_only: bool = False) -> list[Book]:
    if not query:
        return []
    if not google_only:
        db_books = _search_books_from_database(query=query, max_results=max_results)

        if db_books:
            return db_books

    google_books_data = _search_books_from_google_api(query=query, max_results=max_results)

    google_books = []
    for book_data in google_books_data:
        google_books.append(Book(**book_data))

    return google_books

def _search_books_from_google_api(query: str, max_results: int=5) -> list[dict]:
    try:
        response = requests.get(
            GOOGLE_BOOKS_API_URL, 
            params={"q": query, "maxResults": max_results, "key": GOOGLE_BOOKS_API_KEY}
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Error with Google API: {err}")
        data = {}
    books_data = []

    items = data.get("items") or []
    for item in items:
        volume_info = item.get("volumeInfo") or {}
        image_links = volume_info.get("imageLinks") or {}

        author_list = volume_info.get("authors") or []
        genre_list = volume_info.get("categories") or []

        books_data.append(
            {
                "google_book_id": item.get("id"),
                "title": volume_info.get("title"),
                "author": ", ".join(author_list) if author_list else "Unknown",
                "cover_url": image_links.get("thumbnail"),
                "description": volume_info.get("description"),
                "genres": ", ".join(genre_list) if genre_list else None,
                "page_count": volume_info.get("pageCount")
            }
        )

    return books_data

def _search_books_from_database(query: str, max_results: int=5) -> list[Book]:
    with get_session() as session:
        words = query.strip().split()

        if not words:
            return []

        conditions = []
        for word in words:
            pattern = f"%{word}%"
            conditions.append(
                or_(
                    Book.title.ilike(pattern),
                    Book.author.ilike(pattern)
                )
            )

        stmt = select(Book).where(and_(*conditions)).limit(max_results)
        matching_books = list(session.scalars(stmt).all())

        return matching_books or []


if __name__ ==  "__main__":
    result = _search_books_from_google_api("1984 George Orwell")

    for i, book in enumerate(result, 1):
        print(f"\n--- Book {i} ---")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"ID: {book['google_book_id']}")