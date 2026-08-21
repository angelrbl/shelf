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

def toggle_dark_mode(ui_mode: str) -> None:
    dark = ui.dark_mode()

    if ui_mode == "dark":
        dark.disable()
        app.storage.user["ui_mode"] = "light"

    else:
        dark.enable()
        app.storage.user["ui_mode"] = "dark"

    return

def apply_theme() -> None:
    hide_scrollbar()

    is_dark = app.storage.user.get("ui_mode", "light")
        
    if is_dark == "dark":
        toggle_dark_mode(ui_mode="light")
    
    ui.colors(primary='#2c3e50', secondary='#18bc9c', accent='#e74c3c')
    ui.query('body').classes('bg-slate-50')

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