from typing import Any
from nicegui import ui

def user_input(label: str, icon: str, password: bool=False, value:str | None = None) -> ui.input:
    base_input = ui.input(label=label, password=password, value=value).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text: str, on_click: function) -> ui.button:
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')

def icon_button(icon: str, color: str, tooltip: str, on_click: callable | None = None) -> ui.button:
    return ui.button(icon=icon, on_click=on_click).props(f'flat round color={color}').tooltip(tooltip)

def user_select(options: dict, label:str | None = None, value: Any | None = None, on_change: callable | None = None, icon: str | None = None) -> ui.select:
    base_select = ui.select(label=label, options=options, value=value, on_change=on_change).classes('w-full')
    with base_select.add_slot('prepend'):
        ui.icon(icon)
    return base_select