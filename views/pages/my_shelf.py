from nicegui import ui, app

from services import get_user_shelf, get_unique_shelf_genres, filter_user_shelf
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
    shelf_header(current_path='/my_shelf')

    user_shelf = get_user_shelf(user_id=app.storage.user.get("user_id"))

    def handle_filter_shelf(query: str | None = None, state: BookState | None = None, genre: str | None = None):
        filtered_shelf = filter_user_shelf(shelf=user_shelf, query=query, state=state, genre=genre)
        render_shelf.refresh(user_shelf=filtered_shelf)

    with ui.column().classes('max-w-7xl w-full mx-auto px-4 md:px-0 py-4 gap-6 items-center'):
        with ui.row().classes('w-full items-center gap-4 justify-between sm:ml-20 sm:pr-20'):
            ui.label("Your shelf:").classes('text-2xl text-slate-700 text text-bold')
            submit_button(text="Add book", on_click=lambda: ui.navigate.to('search')).classes(remove='w-full shadow')

        with ui.row().classes('w-full max-w-6xl items-center gap-3 flex-col sm:flex-row'):
            query = (
                user_input(label="Search your books", icon="search")
                .on('keydown.enter', lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value))
                .on('blur', lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value))
                .classes("sm:flex-1")
                .props(remove='outlined')
            )

            with ui.row().classes('w-full sm:w-auto gap-3 flex-1'):
                state = user_select(
                    label="State",
                    options={None: "All states", **{state: state.value.title() for state in BookState}},
                    value=None,
                    on_change=lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value),
                    icon="bookmark_border"
                ).classes(remove="w-full", add="flex-1 sm:w-44")
                genre = user_select(
                    label="Genre",
                    options={None: "All genres", **{genre.lower(): genre for genre in get_unique_shelf_genres(shelf=user_shelf)}},
                    value=None,
                    on_change=lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value),
                    icon='book'
                ).classes(remove="w-full", add="flex-1 sm:w-44")

        render_shelf(user_shelf=user_shelf, page=1, books_per_page=9)