from typing import Any
from nicegui import ui, app

def user_input(label: str, icon: str, password: bool=False, password_toggle_button: bool=False, value:str | None = None) -> ui.input:
    base_input = ui.input(label=label, password=password, value=value, password_toggle_button=password_toggle_button).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text: str, on_click: function) -> ui.button:
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')

def icon_button(icon: str, color: str, tooltip: str, dark: str | None = None, on_click: callable | None = None) -> ui.button:
    if dark:
        ui_mode = app.storage.user.get("ui_mode", "light")
        color = color if ui_mode == "light" else dark

    return ui.button(icon=icon, on_click=on_click).props(f'flat round color={color}').tooltip(tooltip)

def user_select(options: dict, label:str | None = None, value: Any | None = None, on_change: callable | None = None, icon: str | None = None) -> ui.select:
    base_select = ui.select(label=label, options=options, value=value, on_change=on_change).classes('w-full')
    with base_select.add_slot('prepend'):
        ui.icon(icon)
    return base_select

def section_title(icon:str, text: str) -> None:
    with ui.row().classes('w-full mx-auto justify-start px-1 mt-5 gap-3 items-center'):
        ui.icon(icon, color='slate-600').classes('text-xl')
        ui.label(text).classes('text-md font-black tracking-widest text-slate-600 uppercase')