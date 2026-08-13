import math
from nicegui import ui

from models import UserBook

from views.theme import STATE_COLORS
from views.components.core import section_title
from views.components.books import book_dialog

def user_book_card(user_book: UserBook) -> None:
    user_id = user_book.user_id
    book = user_book.book

    with ui.card().on("click", lambda: book_dialog(user_id=user_id, book=user_book.book, current_user_book=user_book, start_on_form=True)).classes(
        'p-0 w-full h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer flex flex-col'):

        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain shrink-0')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1 flex-1 justify-between flex flex-col w-full'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')

            ui.space()
            
            with ui.row().classes('w-full mt-2 justify-between items-center'):
                current_state = user_book.state
                color_classes = STATE_COLORS.get(current_state, "bg-slate-100 text-slate-700")
                
                ui.badge(user_book.state.value.title()).classes(f'{color_classes} p-1.75').props('rounded')
                if user_book.rating:
                    ui.label(f"{user_book.rating}/10").classes("text-bold text-slate-600 text-bold text-lg")

def add_book_card() -> None:
    with ui.card().on('click', lambda: ui.navigate.to('/search')).classes(
        'w-full h-full min-h-[200px] sm:min-h-[300px] items-center justify-center cursor-pointer '
        'bg-transparent shadow-sm hover:shadow-md border border-dashed border-gray-700'
    ):
        ui.label('+ Add Book').classes('text-gray-700')

def render_currently_reading(user_id: int | None = None, currently_reading_book: UserBook | None = None) -> None:
    if not currently_reading_book:
        return

    if not user_id:
        user_id = currently_reading_book.user_id

    book = currently_reading_book.book

    with ui.column().classes('w-full max-w-4xl mx-auto gap-4 sm:mt-8 px-4'):

        section_title(icon="auto_stories", text="On the nightstand")

        with ui.card().classes('w-full p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-100 bg-white hover:shadow-md transition-all'):
            with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
                    with ui.column().classes('col-span-1 w-full justify-center items-center'):
                        (
                            ui.image(book.cover_url)
                            .classes('w-32 h-44 sm:w-40 sm:h-56 object-cover rounded-xl shadow-md cursor-pointer hover:shadow-xl transition-all')
                            .on("click", lambda: book_dialog(user_id=user_id, book=book))
                        )
            
                    with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
                        ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                        ui.label(book.author).classes('text-lg text-slate-500 font-medium')
            
                        with ui.row().classes('w-full justify-between pr-4 mt-2 mb-4 items-center'):
                            if book.genres:
                                genres = book.genres.split(", ")
                                with ui.row().classes('mt-2 gap-2'):
                                    for genre in genres[0:3]:
                                        ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')
                            ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')
            
                        ui.separator()
                        ui.space()

                        if currently_reading_book.start_date:
                            with ui.row().classes('w-full items-center justify-center sm:justify-start gap-2 text-slate-500'):
                                ui.icon('calendar_today').classes('text-lg')
                                ui.label(f"Started: {currently_reading_book.start_date}").classes('text-sm font-medium')

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