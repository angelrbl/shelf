from nicegui import ui, app

def shelf_header() -> None:
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
