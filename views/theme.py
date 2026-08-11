from nicegui import ui

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

def apply_theme() -> None:
    hide_scrollbar()
    ui.colors(primary='#2c3e50', secondary='#18bc9c', accent='#e74c3c')
    ui.query('body').classes('bg-slate-50')

STATE_COLORS = {
    BookState.READ: "!bg-green-700 text-green-100",
    BookState.WISHED: "!bg-blue-700 text-blue-100",
    BookState.READING: "!bg-orange-800 text-orange-100",
    BookState.DROPPED: "!bg-red-700 text-red-100"
}