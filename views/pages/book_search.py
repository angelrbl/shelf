from nicegui import ui, app

from services import search_books

from views.theme import apply_theme
from views.components import (
    user_input,
    render_header,
    render_mobile_bottom_bar,
    render_books,
    submit_button
)

@ui.page('/search')
def book_search() -> None:
    if not app.storage.user.get('user_id'):
            ui.navigate.to('/login')
            return
        
    apply_theme()
    render_header(current_path='/search')

    with ui.column().classes('max-w-7xl w-full mx-auto px-6 md:px-0 py-4 gap-6 pb-28 sm:pb-4'):
        with ui.row().classes('w-full justify-between items-end'):
            ui.label(f"Search").classes("text-3xl text-slate-700 font-medium")
            
        ui.separator().classes('w-full mb-5')

        query_value = app.storage.user.pop('current_search_query', None)

        def handle_search(search_query: str, max_results: int = 5, google_only: bool = False):
            if not search_query:
                render_books.refresh(books=[])
                return

            books = search_books(query=search_query, max_results=max_results, google_only=google_only)
            render_books.refresh(books=books)

        with ui.row().classes('w-full items-center gap-4 justify-between ml-10 pr-20 mb-10'):
            search_input = (
                user_input(label="Search books", icon="search", value=query_value)
                .classes(remove='w-full', add='flex-1')
                .props(remove='outlined')
                .on("blur", lambda: handle_search(search_query=search_input.value))
                .on("keydown.enter", lambda: handle_search(search_query=search_input.value))
            )
            submit_button(text="Search", on_click=lambda: handle_search(search_query=search_input.value)).classes(remove='w-full shadow')

        if query_value:
            initial_books = search_books(query=query_value)
            render_books(books=initial_books)
        else:
            render_books(books=[])

        with ui.row().classes('w-full items-center gap-1 justify-center mb-10'):
            ui.label("Can't find your books?,").classes('text-lg text-slate-700')
            ui.label("search globally.").on('click', lambda:handle_search(search_query=search_input.value, max_results=10, google_only=True)).classes('text-lg text-slate-700'
            ' hover:text-slate-500 transition-colors cursor-pointer text-bold')

    render_mobile_bottom_bar(current_path='/search')