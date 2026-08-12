from nicegui import ui

from services import total_read_books, average_book_rating, total_read_books_this_year

def stats_card(stat: int | float, label: str) -> None:
    with ui.column().classes('flex-1 text-center items-center gap-0'):
        ui.label(f"{stat}").classes('text-3xl font-black text-slate-800')
        ui.label(label).classes('text-[10px] tracking-wider font-bold text-slate-400 uppercase')

def render_general_stats(user_id: int) -> None:
    with ui.row().classes('max-w-5xl w-full mx-auto justify-around mt-5 bg-slate-100/80 p-6 gap-3 rounded-2xl items-center'):
        ui.label("General stats").classes('w-full font-black text-xl text-slate-700 text-center')

        ui.separator().classes('bg-slate-200/80 my-1 mb-2')
        
        stats_card(stat=total_read_books(user_id=user_id), label="read books")
        stats_card(stat=total_read_books_this_year(user_id=user_id), label="this year")
        stats_card(stat=average_book_rating(user_id=user_id), label="average rating")