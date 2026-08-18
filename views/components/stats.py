from nicegui import ui

from services import total_read_books, average_book_rating, total_read_books_this_year

from views.components.core import section_title

def stats_card(stat: int | float, desktop_label: str, mobile_label: str, border: bool = False) -> None:
    border_class = 'border-r border-slate-200' if border else ''
    with ui.column().classes(f'flex-1 text-center items-center gap-1 sm:p-3 sm:{border_class}'):
        ui.label(f"{stat}").classes('text-2xl sm:text-3xl font-black text-slate-800')
        ui.label(desktop_label).classes('text-[10px] tracking-widest font-bold text-slate-400 uppercase whitespace-nowrap hidden sm:!block')
        ui.label(mobile_label).classes('text-[10px] tracking-widest font-bold text-slate-400 uppercase whitespace-nowrap sm:!hidden')

def render_general_stats(user_id: int) -> None:
    with ui.column().classes('w-full max-w-4xl mx-auto gap-3 px-4 mb-2'):

        section_title(icon='bar_chart', text="general stats")

        with ui.card().classes('w-full rounded-2xl p-6 shadow-sm border border-slate-100 bg-white hover:shadow-md transition-all'):
            with ui.row().classes('w-full justify-around gap-4 items-center'):
                stats_card(stat=total_read_books(user_id=user_id), desktop_label="total read books", mobile_label="books", border=True)  
                stats_card(stat=total_read_books_this_year(user_id=user_id), desktop_label="books read this year", mobile_label="this year", border=True)
                stats_card(stat=f"{average_book_rating(user_id=user_id):.1f}", desktop_label="average rating", mobile_label="avg rating")