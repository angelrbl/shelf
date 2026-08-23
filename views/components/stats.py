from nicegui import ui, app

from services import total_read_books, average_book_rating, total_read_books_this_year, user_books_by_genre, get_heatmap_data

from views.components.core import section_title
from views.theme import CHART_COLORS_DARK, CHART_COLORS_LIGHT

def stats_card(stat: int | float, desktop_label: str, mobile_label: str, border: bool = False) -> None:
    border_class = 'border-r border-slate-200 dark:border-neutral-700' if border else ''
    with ui.column().classes(f'flex-1 text-center items-center gap-1 sm:p-3 sm:{border_class}'):
        ui.label(f"{stat}").classes('text-2xl sm:text-3xl font-black text-slate-800 dark:text-neutral-100')
        ui.label(desktop_label).classes('text-[10px] tracking-widest font-bold text-slate-400 dark:text-neutral-500 uppercase whitespace-nowrap hidden sm:!block')
        ui.label(mobile_label).classes('text-[10px] tracking-widest font-bold text-slate-400 dark:text-neutral-500 uppercase whitespace-nowrap sm:!hidden')

def books_by_genre_piechart(user_id: int, ui_mode: str = 'light'):
    raw_books_by_genre = user_books_by_genre(user_id=user_id)

    colors = CHART_COLORS_DARK if ui_mode == "dark" else CHART_COLORS_LIGHT

    data = [{'name': genre, 'value': value} for genre, value in raw_books_by_genre.items()]

    ui.echart({
        'color': colors['pie_series'],
        'tooltip': {'trigger': 'item'},
        'legend': {
            'bottom': '0%',
            'left': 'center',
            'icon': 'circle',
            'textStyle': {'color': colors['legend_text']}
        },
        'series': [
            {
                'name': 'Genres',
                'type': 'pie',
                'radius': ['45%', '70%'],
                'center': ['50%', '42%'],
                'itemStyle': {
                    'borderRadius': 8,
                    'borderColor': colors['pie_border'],
                    'borderWidth': 3
                },
                'label': {'show': False},
                'data': data,
            }
        ]
    }).classes('w-full h-80')

def pages_read_heatmap(user_id: int, ui_mode: str = 'light') -> None:

    data = get_heatmap_data(user_id=user_id)

    colors = CHART_COLORS_DARK if ui_mode == "dark" else CHART_COLORS_LIGHT

    def get_max_pages(data: list) -> int:
        max_value = 0
        for entry in data:
            max_value = max(max_value, entry[1])
        return max_value

    ui.echart({
        'tooltip': {
            'position': 'top',
            'formatter': ' {c} pages read this day'
        },
        'visualMap': {
            'min': 0,
            'max': get_max_pages(data=data),
            'calculable': True,
            'orient': 'horizontal',
            'left': 'center',
            'bottom': '0%',
            'inRange': {'color': colors['heatmap_gradient']}
        },
        'calendar': {
            'top': 30,
            'bottom': 60,
            'left': 40,
            'right': 20,
            'range': '2026',
            'cellSize': ['auto', 16],
            'itemStyle': {
                'color': colors['heatmap_empty'],
                'borderWidth': 3,
                'borderColor': colors['heatmap_border']
            },
            'yearLabel': {'show': False},
            'splitLine': {'show': False}
        },
        'series': {
            'type': 'heatmap',
            'coordinateSystem': 'calendar',
            'data': data
        }
    }).classes('w-full h-64')

def render_insights(user_id: int) -> None:
    with ui.column().classes('w-full max-w-4xl mx-auto gap-3 px-4 mb-2'):

        section_title(icon='insights', text="insights")

        with ui.card().classes('w-full rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-neutral-800 bg-white dark:!bg-neutral-800/60 hover:shadow-md transition-all'):
            with ui.row().classes('w-full justify-around gap-4 items-center'):
                stats_card(stat=total_read_books(user_id=user_id), desktop_label="total read books", mobile_label="books", border=True)  
                stats_card(stat=total_read_books_this_year(user_id=user_id), desktop_label="books read this year", mobile_label="this year", border=True)
                stats_card(stat=f"{float(average_book_rating(user_id=user_id)):.1f}", desktop_label="average rating", mobile_label="avg rating")

def render_user_stats(user_id: int) -> None:
    with ui.column().classes('w-full mx-auto gap-4 px-4 mt-4'):
    
        section_title(icon="bar_chart", text="your stats")

        @ui.refreshable
        def user_stats():
            ui_mode = app.storage.user.get('ui_mode', 'light')

            with ui.row().classes('w-full flex flex-col sm:flex-row gap-4 items-stretch'):
                with ui.card().classes('w-full sm:w-[350px] shrink-0 p-6 rounded-2xl shadow-sm border border-slate-100 '
                'dark:border-neutral-800 bg-white dark:!bg-neutral-800/60 hover:shadow-md transition-all flex flex-col'):
                    with ui.column().classes('w-full justify-between items-center'):
                        ui.label("Read books by genre").classes('text-lg font-bold text-slate-700 dark:text-neutral-200')
                        books_by_genre_piechart(user_id=user_id, ui_mode=ui_mode)

                with ui.card().classes('w-full flex-1 p-6 rounded-2xl shadow-sm border border-slate-100 '
                'dark:border-neutral-800 bg-white dark:!bg-neutral-800 hover:shadow-md transition-all overflow-x-auto flex flex-col'):
                    with ui.column().classes('w-full min-w-[600px]'):
                        ui.label("Average pages read this year").classes('text-lg font-bold text-slate-700 dark:text-neutral-200 self-start sm:self-center mb-2')
                        pages_read_heatmap(user_id=user_id, ui_mode=ui_mode)

            app.storage.client['stats_refresh'] = user_stats.refresh

        user_stats()