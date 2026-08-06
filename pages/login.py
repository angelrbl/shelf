from nicegui import ui, app
from services import authenticate_user, register_user

@ui.page('/login')
def login_page():
    username_input = ui.input('User')
    password_input = ui.input('Password', password=True)

    def handle_login():
        try:
            user = authenticate_user(username=username_input.value, password=password_input.value)
            app.storage.user['user_id'] = user.id
            ui.navigate.to('/')
        except ValueError as err:
            ui.notify(str(err), color="negative")

    ui.button("Log in", on_click=handle_login)