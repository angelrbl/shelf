import requests
from core import GOOGLE_BOOKS_API_KEY

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

def search_books(query: str, max_results: int=5) -> list[dict]:
    response = requests.get(
        GOOGLE_BOOKS_API_URL, 
        params={"q": query, "maxResults": max_results, "key": GOOGLE_BOOKS_API_KEY}
    )
    response.raise_for_status()
    data = response.json()

    books = []

    items = data.get("items") or []
    for item in items:
        volume_info = item.get("volumeInfo") or {}
        image_links = volume_info.get("imageLinks") or {}

        author_list = volume_info.get("authors") or []
        genre_list = volume_info.get("categories") or []

        books.append(
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

    return books

if __name__ ==  "__main__":
    result = search_books("1984 George Orwell")

    for i, book in enumerate(result, 1):
        print(f"\n--- Book {i} ---")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"ID: {book['google_book_id']}")