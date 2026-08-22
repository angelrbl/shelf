from nicegui import ui, app

from models import BookState

def hide_scrollbar():
    ui.add_head_html('''
        <style>
            ::-webkit-scrollbar {
                display: none;
            }
            * {
                -ms-overflow-style: none;
                scrollbar-width: none;
            }
        </style>
    ''')


def toggle_dark_mode() -> None:
    dark = app.storage.client.get("dark", None)
    if not dark:
        dark = ui.dark_mode()

    dark.toggle()

    app.storage.user["ui_mode"] = "dark" if dark.value else "light"

def apply_theme() -> None:
    hide_scrollbar()

    ui_mode = app.storage.user.get("ui_mode", "light")

    dark = ui.dark_mode()
    app.storage.client["dark"] = dark
        
    if ui_mode == "dark":
        toggle_dark_mode()
    ui.colors(
        primary='#2c3e50',
        secondary='#18bc9c',
        accent='#e74c3c',
        dark='#262626',
        dark_page='#171717',
    )
    ui.query('body').classes('bg-slate-50 dark:bg-neutral-900')

STATE_COLORS = {
    BookState.READ: "!bg-green-700 text-green-100",
    BookState.WISHED: "!bg-blue-700 text-blue-100",
    BookState.READING: "!bg-orange-800 text-orange-100",
    BookState.DROPPED: "!bg-red-700 text-red-100"
}

RANK_COLORS = {
    1: 'text-amber-500',
    2: 'text-zinc-500',
    3: 'text-orange-800'
}