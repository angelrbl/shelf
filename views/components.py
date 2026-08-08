from nicegui import ui, app

def user_input(label, icon, password=False):
    base_input = ui.input(label=label, password=password).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text, on_click):
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')

def shelf_header():
    def go_home():
        ui.navigate.to('/')
        
    def log_out():
        app.storage.user.clear()
        go_home()
    
    with ui.header(fixed=False, bordered=True).classes('bg-transparent p-3').props('reveal'):
        with ui.row().classes('w-full items-center'):
            ui.label("Shelf.").on('click', go_home).classes('text-3xl font-bold text-slate-700 text pl-5 hover:text-slate-500 cursor-pointer')
            ui.space()
            ui.label("Log out").on('click', log_out).classes('cursor-pointer text-xl text-slate-700 text pr-5 hover:text-slate-500')