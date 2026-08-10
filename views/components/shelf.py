import math
from nicegui import ui

from models import UserBook

from views.components.books import book_dialog

def user_book_card(user_book: UserBook) -> None:
    user_id = user_book.user_id
    book = user_book.book

    with ui.card().on("click", lambda: book_dialog(user_id=user_id, book=user_book.book, current_user_book=user_book, start_on_form=True)).classes(
        'p-0 w-full h-56 sm:h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer'):

        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1 justify-between'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')

            ui.space()
            
            with ui.row().classes('mt-2'):
                ui.badge(user_book.state.value.title()).classes('p-1.75').props('rounded')

def add_book_card() -> None:
    with ui.card().on('click', lambda: ui.navigate.to('/search')).classes(
        'w-full h-full min-h-[200px] sm:min-h-[300px] items-center justify-center cursor-pointer '
        'bg-transparent shadow-sm hover:shadow-md border border-dashed border-gray-700'
    ):
        ui.label('+ Add Book').classes('text-gray-700')

@ui.refreshable
def render_shelf(user_shelf: list, page: int = 1, books_per_page: int = 9) -> None:
    total_books = len(user_shelf)
    total_pages = max(1, math.ceil(total_books / books_per_page))

    page = min(page, total_pages)

    start_idx = (page - 1) * books_per_page
    end_idx = start_idx + books_per_page

    books_for_current_page = user_shelf[start_idx:end_idx]

    with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-10 pt-0'):
        for user_book in books_for_current_page:
            user_book_card(user_book=user_book)

        add_book_card()

    if total_pages > 1:
        with ui.row().classes('w-full justify-center mt-8 mb-4'):
            ui.pagination(
                min=1,
                max=total_pages,
                value=page,
                on_change=lambda e: render_shelf.refresh(user_shelf=user_shelf, page=e.value, books_per_page=books_per_page)
            ).props('rounded color=slate-7')