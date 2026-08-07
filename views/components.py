from nicegui import ui

def user_input(label, icon, password=False):
    base_input = ui.input(label=label, password=password).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text, on_click):
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')