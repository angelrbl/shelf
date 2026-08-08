from nicegui import ui, app

from views.theme import apply_theme
from views.components import shelf_header

@ui.page('/my_shelf')
def my_shelf_page():
    apply_theme()
    
    shelf_header()