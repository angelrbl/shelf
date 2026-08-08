from nicegui import ui, app

from models import UserBook

def user_input(label: str, icon: str, password: bool=False) -> ui.input:
    base_input = ui.input(label=label, password=password).classes('w-full').props('outlined')
    with base_input.add_slot('prepend'):
        ui.icon(icon)
    return base_input

def submit_button(text: str, on_click: function) -> ui.button:
    return ui.button(text=text, on_click=on_click).classes('w-full shadow rounded-lg pt-2 pb-2')

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

def book_card(user_book: UserBook) -> None:
    book = user_book.book

    with ui.card().classes('p-0 w-56 overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md'):
        ui.image(book.cover_url).classes('h-72 w-full object-contain')
        with ui.column().classes('p-3 gap-1'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')
            with ui.row().classes('mt-2'):
                ui.badge(user_book.state.value.title()).classes('p-1.75').props('rounded')