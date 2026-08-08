from nicegui import ui, app

from services import get_user_shelf

from views.theme import apply_theme
from views.components import shelf_header, book_card, add_book_card, user_input, submit_button

@ui.page('/my_shelf')
def my_shelf_page() -> None:
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
        return
    
    apply_theme()
    shelf_header()

    with ui.column().classes('max-w-7xl w-full mx-auto px-6 md:px-0 py-4 gap-6'):
        with ui.row().classes('w-full items-center gap-4 justify-between ml-10 pr-20'):
            query = user_input(label="Search books", icon="search").classes(remove='w-full', add='flex-1').props(remove='outlined')
            submit_button(text="Add book", on_click=lambda: ui.notify("Add a book!")).classes(remove='w-full shadow')

        ui.label("Your books:").classes('text-xl text-slate-700 text text-bold ml-10')

        with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-10 pt-0'):
            user_shelf = get_user_shelf(user_id=app.storage.user.get("user_id"))
            for user_book in user_shelf:
                book_card(user_book=user_book)

            add_book_card()