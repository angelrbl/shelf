import math
from nicegui import ui, app

from models import Book, BookState, UserBook
from services import get_user_book_by_google_id

from views.components.book_dialog import book_dialog

def book_card(book: Book) -> None:
    user_id = app.storage.user.get("user_id")
    user_book = get_user_book_by_google_id(user_id=user_id, google_book_id=book.google_book_id)

    with ui.card().on('click', lambda: book_dialog(user_id=user_id, book=book, current_user_book=user_book)).classes(
        'p-0 w-full h-full flex flex-col overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer'):

        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain shrink-0')
        with ui.column().classes('w-full p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1 justify-between flex-1 flex flex-col'):
            with ui.column().classes('w-full gap-0 items-start'):
                with ui.row().classes('w-full items-start justify-between mt-0 mb-1'):
                    ui.label(book.title).classes('font-semibold text-sm line-clamp-2 flex-1')
                    if user_book:
                        ui.icon('bookmark_added').classes('text-slate-500 text-lg shrink-0')
                ui.label(book.author).classes('text-xs text-slate-500')

            if book.genres:
                genres = book.genres.split(", ")
                end_idx = min(3, len(genres))
                with ui.row().classes('w-full mt-auto pt-2 items-center gap-1'):
                    for genre in genres[0:end_idx]:
                        ui.badge(genre.title()).classes('p-1.75').props('rounded')

@ui.refreshable
def render_books(books: list, page: int = 1, books_per_page: int = 10) -> None:
    if not books:
        return

    total_books = len(books)
    total_pages = max(1, math.ceil(total_books / books_per_page))

    page = min(page, total_pages)

    start_idx = (page - 1) * books_per_page
    end_idx = start_idx + books_per_page

    books_for_current_page = books[start_idx:end_idx]

    with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-10 pt-0'):
        for book in books_for_current_page:
            book_card(book=book)

    if total_pages > 1:
        with ui.row().classes('w-full justify-center mt-8 mb-2'):
            ui.pagination(
                min=1,
                max=total_pages,
                value=page,
                on_change=lambda e: render_books.refresh(books=books, page=e.value, books_per_page=books_per_page)
            ).props('rounded color=slate-7')