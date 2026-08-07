from nicegui import ui

def apply_theme():
    ui.colors(primary='#2c3e50', secondary='#18bc9c', accent='#e74c3c')
    ui.query('body').classes('bg-slate-50')