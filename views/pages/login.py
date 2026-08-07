from nicegui import ui, app
from services import authenticate_user, register_user
from views.theme import apply_theme

@ui.page('/login')
def login_page():
    apply_theme()
    
    with ui.card().classes('absolute-center w-100 shadow-lg rounded-lg'):
        ui.label("Shelf.").classes('text-3xl font-bold w-full mb-4 text-slate-700 text-center pt-5')
        with ui.tabs().classes('w-full') as tabs:
            login_tab = ui.tab('Log In', icon='login')
            register_tab = ui.tab('Register', icon='person_add')

        with ui.tab_panels(tabs, value=login_tab).classes('w-full bg-transparent'):
            
            # Log in tab
            with ui.tab_panel(login_tab):
                login_user = ui.input('User').classes('w-full').props('outlined')
                login_password = ui.input('Password', password=True).classes('w-full').props('outlined')

                def handle_login():
                    try:
                        user = authenticate_user(username=login_user.value, password=login_password.value)
                        app.storage.user['user_id'] = user.id
                        ui.navigate.to('/')
                    except ValueError as err:
                        ui.notify(str(err), color="negative")

                ui.button("Log in", on_click=handle_login).classes('w-full mt-4 rounded-lg')

            # Register tab
            with ui.tab_panel(register_tab):
                reg_user = ui.input('User').classes('w-full').props('outlined')
                reg_password = ui.input('Password', password=True).classes('w-full').props('outlined')
                reg_password_repeat = ui.input('Repeat password', password=True).classes('w-full').props('outlined')

                def handle_register():
                    if reg_password.value != reg_password_repeat.value:
                        ui.notify('Passwords given do not match.', color='warning')
                        return

                    try:
                        register_user(username=reg_user.value, password=reg_password.value)
                        ui.notify("Account created successfully! Please, log in.")

                        reg_user.value, reg_password.value, reg_password_repeat.value = '', '', ''
                        tabs.set_value(login_tab)
                    except ValueError as err:
                        ui.notify(str(err), color="negative")

                ui.button("Make account", on_click=handle_register).classes('w-full mt-4 rounded-lg')