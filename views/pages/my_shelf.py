from nicegui import ui, app

from services import get_user_shelf

from views.theme import apply_theme
from views.components import (
    shelf_header,
    user_input,
    submit_button,
    render_shelf
)

@ui.page('/my_shelf')
def my_shelf_page() -> None:
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
        return
    
    apply_theme()
    shelf_header()

    def handle_search():
        if query.value:
            app.storage.user['current_search_query'] = query.value
        ui.navigate.to('/search')

    with ui.column().classes('max-w-7xl w-full mx-auto px-6 md:px-0 py-4 gap-6'):
        with ui.row().classes('w-full items-center gap-4 justify-between ml-10 pr-20'):
            query = user_input(label="Search your books", icon="search").classes(remove='w-full', add='flex-1').props(remove='outlined')
            submit_button(text="Add book", on_click=handle_search).classes(remove='w-full shadow')

        ui.label("Your shelf:").classes('text-xl text-slate-700 text text-bold ml-10')

        user_shelf = get_user_shelf(user_id=app.storage.user.get("user_id"))
        render_shelf(user_shelf=user_shelf, page=1, books_per_page=9)