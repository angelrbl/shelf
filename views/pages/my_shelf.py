from nicegui import ui, app

from services import get_user_shelf
from models import BookState

from views.theme import apply_theme
from views.components import (
    shelf_header,
    user_input,
    submit_button,
    render_shelf,
    user_select
)

@ui.page('/my_shelf')
def my_shelf_page() -> None:
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
        return
    
    apply_theme()
    shelf_header()

    with ui.column().classes('max-w-7xl w-full mx-auto px-6 md:px-0 py-4 gap-6'):
        with ui.row().classes('w-full items-center gap-4 justify-between ml-10 pr-20'):
            ui.label("Your shelf:").classes('text-2xl text-slate-700 text text-bold')
            submit_button(text="Add book", on_click=lambda: ui.navigate.to('search')).classes(remove='w-full shadow')

        with ui.row().classes('w-full max-w-6xl items-center justify-between gap-2'):
            query = user_input(label="Search your books", icon="search").classes(remove="w-full", add="flex-1").props(remove='outlined')
            state = user_select(
                label="State",
                options={None: "All states", **{state: state.value.title() for state in BookState}},
                value=None,
                icon="bookmark_border"
            ).classes(remove="w-full", add="h-1/4")

        user_shelf = get_user_shelf(user_id=app.storage.user.get("user_id"))
        render_shelf(user_shelf=user_shelf, page=1, books_per_page=9)