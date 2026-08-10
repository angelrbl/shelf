from nicegui import ui

def user_input(label: str, icon: str, password: bool=False, value:str | None = None) -> ui.input:
    base_input = ui.input(label=label, password=password, value=value).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text: str, on_click: function) -> ui.button:
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')