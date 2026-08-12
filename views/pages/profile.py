from nicegui import ui, app

from services import get_user_by_id

from views.theme import apply_theme
from views.components import (
    render_header,
    render_mobile_bottom_bar,
    icon_button,
    render_general_stats
)

@ui.page('/profile')
def profile_page() -> None:
    if not app.storage.user.get('user_id'):
        ui.navigate.to('/login')
        return

    apply_theme()
    render_header(current_path='/profile')

    user = get_user_by_id(user_id=app.storage.user.get("user_id"))

    with ui.column().classes('max-w-7xl w-full mx-auto px-4 md:px-0 py-4 gap-6 items-center pb-28 sm:pb-4'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label(f"@{user.username}").classes("text-3xl text-slate-700 font-bold")

            icon_button(icon='settings', color='slate-500', on_click=lambda: ui.notify("Opening settings!", type="positive"), tooltip="Open settings").classes('text-lg')

            ui.separator().classes('w-full')

        render_general_stats(user_id=user.id)


    render_mobile_bottom_bar(current_path='/profile')