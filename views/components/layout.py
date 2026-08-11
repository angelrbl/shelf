from nicegui import ui, app

NAV_ITEMS = [
    {'label': 'My Shelf', 'icon': 'dashboard', 'path': '/my_shelf'},
    {'label': 'Search', 'icon': 'search', 'path': '/search'},
]

def shelf_header(current_path: str) -> None:
    def go_home():
        ui.navigate.to('/')
        
    def log_out():
        app.storage.user.clear()
        go_home()

    with ui.header(fixed=True, bordered=True).classes('bg-slate-50/60 backdrop-blur-md p-3 z-50').props('reveal'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label("Shelf.").on('click', go_home).classes('text-3xl font-bold text-slate-700 text pl-5 hover:text-slate-500 cursor-pointer')

            with ui.row().classes('hidden sm:!flex items-center gap-6'):
                for item in NAV_ITEMS:
                    is_active = current_path == item["path"]
                    color = 'text-slate-900 font-bold hover:text-slate-700' if is_active else 'text-slate-500 hover:text-slate-800'

                    with ui.row().on('click', lambda _, path=item['path']: ui.navigate.to(path)).classes(f'items-center gap-2 cursor-pointer {color}'):
                        ui.icon(item['icon']).classes('text-xl')
                        ui.label(item['label']).classes('text-sm')

            ui.label("Log out").on('click', log_out).classes('cursor-pointer text-xl text-slate-700 text pr-5 hover:text-slate-500')