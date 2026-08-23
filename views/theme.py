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

    if dark.value:
        app.storage.user["ui_mode"] = "dark"
    else:
        app.storage.user.pop('ui_mode', 'light')

    if 'stats_refresh' in app.storage.client:
        app.storage.client['stats_refresh']()

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
    BookState.READING: "!bg-orange-800 text-orange-100 dark:!bg-orange-700",
    BookState.DROPPED: "!bg-red-700 text-red-100"
}

RANK_COLORS = {
    1: 'text-amber-500',
    2: 'text-zinc-500 dark:!text-zinc-400',
    3: 'text-orange-800 dark:!text-orange-700'
}

CHART_COLORS_LIGHT = {
    'pie_series': ['#6366f1', '#3b82f6', '#14b8a6', '#f59e0b', '#f43f5e', '#8b5cf6'],
    'pie_border': '#ffffff',
    'legend_text': '#475569',
    'heatmap_gradient': ['#e0e7ff', '#818cf8', '#312e81'],
    'heatmap_empty': '#f8fafc',
    'heatmap_border': '#ffffff',
}

CHART_COLORS_DARK = {
    'pie_series': ['#818cf8', '#60a5fa', '#2dd4bf', '#fbbf24', '#fb7185', '#a78bfa'],
    'pie_border': '#262626',
    'legend_text': '#d4d4d4',
    'heatmap_gradient': ['#312e81', '#818cf8', '#c7d2fe'],
    'heatmap_empty': '#262626',
    'heatmap_border': '#404040',
}