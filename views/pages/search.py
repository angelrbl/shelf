from nicegui import ui, app

from services import search_books, search_users

from views.theme import apply_theme
from views.components import (
    user_input,
    render_header,
    render_mobile_bottom_bar,
    render_books,
    render_search_users,
    submit_button
)

@ui.page('/search')
def search_page() -> None:
    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.navigate.to('/login')
        return
        
    apply_theme()
    render_header(current_path='/search')

    with ui.column().classes('max-w-7xl w-full mx-auto px-6 md:px-0 py-4 gap-0 pb-28 sm:pb-4'):
        query_value = app.storage.user.pop('current_search_query', None)

        def handle_search(search_query: str, max_results: int = 5, google_only: bool = False):
            if not search_query:
                render_books.refresh(books=[])
                render_search_users.refresh(users=[], user_id=user_id)
                return

            if search_query[0] == '@':
                clean_query = search_query[1:]

                users = search_users(query=clean_query)
                render_search_users.refresh(users=users, user_id=user_id)
                render_books.refresh(books=[])
            else:
                users = search_users(query=search_query)
                render_search_users.refresh(users=users, user_id=user_id)

                books = search_books(query=search_query, max_results=max_results, google_only=google_only)
                render_books.refresh(books=books, on_search=lambda:handle_search(search_query=search_input.value, max_results=10, google_only=True))

        with ui.row().classes('w-full items-center gap-4 justify-between ml-10 pr-20 mb-4 sm:mb-6'):
            search_input = (
                user_input(label="Search anything", icon="search", value=query_value)
                .classes(remove='w-full', add='flex-1')
                .props(remove='outlined')
                .on("keydown.enter", lambda: handle_search(search_query=search_input.value))
            )
            submit_button(text="Search", on_click=lambda: handle_search(search_query=search_input.value)).classes(remove='w-full shadow')

        if query_value:
            if query_value[0] == '@':
                clean_query = query_value[1:]
                initial_users = search_users(query=clean_query)
                render_search_users(users=initial_users, user_id=user_id)
            else:
                initial_users = search_users(query=query_value)
                render_search_users(users=initial_users, user_id=user_id)

                initial_books = search_books(query=query_value)
                render_books(books=initial_books, on_search=lambda:handle_search(search_query=search_input.value, max_results=10, google_only=True))
        else:
            render_search_users(users=[], user_id=user_id)
            render_books(books=[])

    render_mobile_bottom_bar(current_path='/search')