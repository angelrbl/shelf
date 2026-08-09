import math
from nicegui import ui, app

from models import UserBook, Book

def user_input(label: str, icon: str, password: bool=False, value:str | None = None) -> ui.input:
    base_input = ui.input(label=label, password=password, value=value).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text: str, on_click: function) -> ui.button:
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')

def shelf_header() -> None:
    def go_home():
        ui.navigate.to('/')
        
    def log_out():
        app.storage.user.clear()
        go_home()
    
    with ui.header(fixed=False, bordered=True).classes('bg-transparent p-3').props('reveal'):
        with ui.row().classes('w-full items-center'):
            ui.label("Shelf.").on('click', go_home).classes('text-3xl font-bold text-slate-700 text pl-5 hover:text-slate-500 cursor-pointer')
            ui.space()
            ui.label("Log out").on('click', log_out).classes('cursor-pointer text-xl text-slate-700 text pr-5 hover:text-slate-500')

def user_book_card(user_book: UserBook) -> None:
    book = user_book.book

    with ui.card().classes('p-0 w-full h-56 sm:h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer'):
        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')
            with ui.row().classes('mt-2'):
                ui.badge(user_book.state.value.title()).classes('p-1.75').props('rounded')

def add_book_card() -> None:
    with ui.card().on('click', lambda: ui.navigate.to('/search')).classes(
        'w-full h-full min-h-[200px] sm:min-h-[300px] items-center justify-center cursor-pointer '
        'bg-transparent shadow-sm hover:shadow-md border border-dashed border-gray-700'
    ):
        ui.label('+ Add Book').classes('text-gray-700')

def book_card(book: Book) -> None:
    with ui.card().on('click', lambda: book_dialog(book=book)).classes('p-0 w-full h-56 sm:h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer'):
        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')
            if book.genres:
                genres = book.genres.split(", ")
                end_idx = min(3, len(genres))
                with ui.row().classes('mt-2'):
                    for genre in genres[0:end_idx]:
                        ui.badge(genre.title()).classes('p-1.75').props('rounded')

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

@ui.refreshable
def render_books(books: list, page: int = 1, books_per_page: int = 10) -> None:
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

def book_dialog(book: Book) -> None:
    with ui.dialog().classes('items-end sm:items-center !mb-0') as dialog:
        with ui.card().classes('w-full sm:max-w-3xl !pb-0 p-6 flex flex-col gap-4 '
            '!mb-0 mt-auto sm:!my-auto max-h-[95vh] sm:max-h-[85vh] '
            'rounded-t-3xl sm:rounded-2xl rounded-b-3xl sm:rounded-b-2xl'):

            with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):

                with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
                    ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-cover rounded-lg shadow-md')

                with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-bewteen gap-1'):
                    ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                    ui.label(book.author).classes('text-lg text-slate-500 font-medium')

                    if book.genres:
                        genres = book.genres.split(", ")
                        with ui.row().classes('mt-2 gap-2'):
                            for genre in genres[0:3]:
                                ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')

                    ui.space()

                    ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

                    submit_button(text="+ Add book", on_click=lambda: ui.notify("Adding book")).classes('w-full sm:w-auto mt-1 py-2 px-6 rounded-lg shadow-sm font-bold')

            ui.label("Book info:").classes('font-bold text-slate-800 mt-4 text-lg')

            with ui.scroll_area().classes('w-full flex-grow h-48 sm:h-56 pr-4'):
                ui.label(book.description).classes('text-slate-600 leading-relaxed text-justify')

    dialog.open()