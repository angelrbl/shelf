from nicegui import ui, app

from views.theme import toggle_dark_mode
from views.components.core import icon_button

NAV_ITEMS = [
    {'label': 'My Shelf', 'icon': 'dashboard', 'path': '/my_shelf'},
    {'label': 'Search', 'icon': 'search', 'path': '/search'},
    {'label': 'Profile', 'icon': 'person', 'path': '/profile'},
]

def render_header(current_path: str) -> None:
    def go_home():
        ui.navigate.to('/')
        
    def log_out():
        app.storage.user.pop('user_id', None)
        go_home()

    ui_mode = app.storage.user.get("ui_mode", "light")

    with ui.header(fixed=True, bordered=True).classes('bg-slate-50/60 dark:bg-neutral-900/60 backdrop-blur-md p-3 z-50').props('reveal'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label("Shelf.").on('click', go_home).classes('text-3xl font-bold text-slate-700 dark:text-neutral-200 '
            'text pl-5 hover:text-slate-500 hover:dark:text-neutral-400 cursor-pointer')

            with ui.row().classes('hidden sm:!flex items-center gap-8'):
                for item in NAV_ITEMS:
                    is_active = current_path == item["path"]
                    if is_active:
                        color = 'text-slate-900 dark:text-neutral-50 font-bold hover:text-slate-700 hover:dark:text-neutral-300'
                    else:
                        color = 'text-slate-500 hover:text-slate-800 dark:text-neutral-400 dark:hover:text-neutral-100'

                    with ui.row().on('click', lambda _, path=item['path']: ui.navigate.to(path)).classes(f'items-center gap-2 cursor-pointer {color}'):
                        ui.icon(item['icon']).classes('text-xl')
                        ui.label(item['label']).classes('text-sm')

            @ui.refreshable
            def header_buttons(ui_mode: str):
                with ui.row().classes('gap-3 items-center justify-between'):
                    icon_button(
                        icon=("brightness_medium" if ui_mode == "dark" else "dark_mode"),
                        on_click=lambda: (toggle_dark_mode(), header_buttons.refresh(ui_mode="dark" if ui_mode == "light" else "light")),
                        color="slate-600",
                        dark="neutral-300",
                        tooltip=("Toggle light mode" if ui_mode == "dark" else "Toggle dark mode"))
                    ui.label("Log out").on('click', log_out).classes('cursor-pointer text-xl text-slate-700 dark:text-neutral-200 text pr-5 hover:text-slate-500 hover:dark:text-neutral-400')

            header_buttons(ui_mode=ui_mode)

def render_mobile_bottom_bar(current_path: str) -> None:
    with ui.row().classes(
        'fixed bottom-6 left-1/2 -translate-x-1/2 z-50 '
        'bg-white/85 dark:bg-neutral-800/85 backdrop-blur-md border border-slate-200 dark:border-neutral-700 '
        'px-8 py-3 rounded-full shadow-2xl w-[75%] max-w-xs'
        'items-center justify-around '
        'flex sm:!hidden'
    ):
        for item in NAV_ITEMS:
            is_active = current_path == item['path']

            color = 'text-slate-900 dark:text-neutral-50' if is_active else 'text-slate-400 dark:text-neutral-500'
            scale = 'scale-120' if is_active else 'scale-100'

            with ui.column().on('click', lambda _, path=item['path']: ui.navigate.to(path)).classes(
                f"items-center justify-center gap-1 cursor-pointer transition-all {color} {scale}"
            ):
                ui.icon(item['icon']).classes('text-2xl')

                if is_active:
                    ui.icon('circle').classes('text-[6px] text-sky-400')
                else:
                    ui.icon('circle').classes('text-[6px] opacity-0')