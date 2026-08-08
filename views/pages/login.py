from nicegui import ui, app
from services import authenticate_user, register_user

from views.theme import apply_theme
from views.components import user_input, submit_button

@ui.page('/login')
def login_page() -> None:
    apply_theme()
    
    with ui.card().classes('absolute-center w-100 shadow-lg rounded-lg'):
        ui.label("Shelf.").classes('text-3xl font-bold w-full mb-4 text-slate-700 text-center pt-5')
        with ui.tabs().classes('w-full') as tabs:
            login_tab = ui.tab('Log In', icon='login')
            register_tab = ui.tab('Register', icon='person_add')

        with ui.tab_panels(tabs, value=login_tab).classes('w-full bg-transparent'):
            
            # Log in tab
            with ui.tab_panel(login_tab):
                login_user = user_input('User', icon='account_circle')
                login_password = user_input('Password', icon='lock', password=True)

                def handle_login():
                    try:
                        user = authenticate_user(username=login_user.value, password=login_password.value)
                        app.storage.user['user_id'] = user.id
                        ui.navigate.to('/')
                    except ValueError as err:
                        ui.notify(str(err), color="negative")

                submit_button('Log in', on_click=handle_login).classes('mt-4')

            # Register tab
            with ui.tab_panel(register_tab):
                reg_user = user_input('User', icon='account_circle')
                reg_password = user_input('Password', icon='lock', password=True)
                reg_password_repeat = user_input('Repeat password', icon="password", password=True)

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

                submit_button(text="Make account", on_click=handle_register).classes('mt-4')