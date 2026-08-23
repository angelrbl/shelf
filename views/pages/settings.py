from nicegui import ui, app

from services import get_user_by_id

from views.theme import apply_theme
from views.components import (
    render_header,
    render_mobile_bottom_bar,
    section_title,
    render_account_settings,
    render_privacy_settings
)

@ui.page('/settings')
def settings_page():
    user_id = app.storage.user.get('user_id')
    user = get_user_by_id(user_id=user_id)

    if not user_id or not user:
        ui.navigate.to('/login')
        return

    apply_theme()
    render_header(current_path='/profile')

    with ui.column().classes('max-w-7xl w-full mx-auto px-4 md:px-0 py-4 gap-6 items-center pb-28 sm:pb-4'):
        with ui.row().classes('w-full justify-between items-end'):
            ui.label(f"Settings").classes("text-3xl text-slate-700 dark:text-neutral-200 font-medium")
            with ui.row().classes('items-center gap-1 cursor-pointer group').on('click', lambda: ui.navigate.to('/profile')):
                ui.icon("arrow_back").classes('text-slate-700 dark:text-neutral-200 font-bold group-hover:text-slate-500 dark:group-hover:text-neutral-400')
                ui.label("Go back").classes('text-slate-700 dark:text-neutral-200 font-bold group-hover:text-slate-500 dark:group-hover:text-neutral-400')

        ui.separator().classes('w-full')

        section_title(icon='account_circle', text="Account settings")
        render_account_settings(user=user)
        
        section_title(icon='key', text="Privacy settings")
        render_privacy_settings(user=user)

    render_mobile_bottom_bar(current_path='/profile')