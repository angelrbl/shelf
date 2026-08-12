from nicegui import ui, app

NAV_ITEMS = [
    {'label': 'My Shelf', 'icon': 'dashboard', 'path': '/my_shelf'},
    {'label': 'Search', 'icon': 'search', 'path': '/search'},
]

def render_header(current_path: str) -> None:
    def go_home():
        ui.navigate.to('/')
        
    def log_out():
        app.storage.user.clear()
        go_home()

    with ui.header(fixed=True, bordered=True).classes('bg-slate-50/60 backdrop-blur-md p-3 z-50').props('reveal'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label("Shelf.").on('click', go_home).classes('text-3xl font-bold text-slate-700 text pl-5 hover:text-slate-500 cursor-pointer')

            with ui.row().classes('hidden sm:!flex items-center gap-8'):
                for item in NAV_ITEMS:
                    is_active = current_path == item["path"]
                    color = 'text-slate-900 font-bold hover:text-slate-700' if is_active else 'text-slate-500 hover:text-slate-800'

                    with ui.row().on('click', lambda _, path=item['path']: ui.navigate.to(path)).classes(f'items-center gap-2 cursor-pointer {color}'):
                        ui.icon(item['icon']).classes('text-xl')
                        ui.label(item['label']).classes('text-sm')

            ui.label("Log out").on('click', log_out).classes('cursor-pointer text-xl text-slate-700 text pr-5 hover:text-slate-500')

def render_mobile_bottom_bar(current_path: str) -> None:
    with ui.row().classes(
        'fixed bottom-6 left-1/2 -translate-x-1/2 z-50 '
        'bg-white/85 backdrop-blur-md border border-slate-200 '
        'px-8 py-3 rounded-full shadow-2xl w-[75%] max-w-xs'
        'items-center justify-around '
        'flex sm:!hidden'
    ):
        for item in NAV_ITEMS:
            is_active = current_path == item['path']

            color = 'text-slate-900' if is_active else 'text-slate-400'
            scale = 'scale-120' if is_active else 'scale-100'

            with ui.column().on('click', lambda _, path=item['path']: ui.navigate.to(path)).classes(
                f"items-center justify-center gap-1 cursor-pointer transition-all {color} {scale}"
            ):
                ui.icon(item['icon']).classes('text-2xl')

                if is_active:
                    ui.icon('circle').classes('text-[6px] text-sky-400')
                else:
                    ui.icon('circle').classes('text-[6px] opacity-0')