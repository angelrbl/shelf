from nicegui import ui, app

from services import get_user_shelf

from views.theme import apply_theme
from views.components import shelf_header, book_card

@ui.page('/my_shelf')
def my_shelf_page() -> None:
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
        return
    
    apply_theme()

    shelf_header()

    user_shelf = get_user_shelf(user_id=app.storage.user.get("user_id"))
    for user_book in user_shelf:
        book_card(user_book=user_book)