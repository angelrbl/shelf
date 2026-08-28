from nicegui import ui, app
from services import authenticate_user, register_user

from views.theme import apply_theme
from views.i18n import _
from views.components import user_input, submit_button

@ui.page('/login')
def login_page() -> None:
    apply_theme()
    
    with ui.card().classes('absolute-center w-80 sm:w-100 shadow-lg rounded-lg'):
        ui.label("Shelf.").classes('text-3xl font-bold w-full mb-4 text-slate-700 dark:text-neutral-200 text-center pt-5')
        with ui.tabs().classes('w-full') as tabs:
            login_tab = ui.tab(_("login_log_in"), icon='login')
            register_tab = ui.tab(_("login_register"), icon='person_add')

        with ui.tab_panels(tabs, value=login_tab).classes('w-full bg-transparent'):
            
            # Log in tab
            with ui.tab_panel(login_tab):
                def handle_login():
                    try:
                        user = authenticate_user(username=login_user.value, password=login_password.value)
                        app.storage.user['user_id'] = user.id
                        ui.navigate.to('/')
                    except ValueError as err:
                        ui.notify(_(str(err), username=login_user.value), color="negative")

                login_user = user_input(_("login_username"), icon='account_circle')
                login_password = user_input(_("login_password"), icon='lock', password=True, password_toggle_button=True).on('keydown.enter', handle_login)

                submit_button(_("login_log_in"), on_click=handle_login).classes('mt-4')

            # Register tab
            with ui.tab_panel(register_tab):
                def handle_register():
                    if reg_password.value != reg_password_repeat.value:
                        ui.notify(_("settings_passwords_do_not_match"), color='warning')
                        return

                    try:
                        register_user(username=reg_user.value, password=reg_password.value)
                        ui.notify(_("login_account_created"))

                        reg_user.value, reg_password.value, reg_password_repeat.value = '', '', ''
                        tabs.set_value(login_tab)
                    except ValueError as err:
                        ui.notify(_(str(err), username=reg_user.value), color="negative")

                reg_user = user_input(_("login_username"), icon='account_circle')
                reg_password = user_input(_("login_password"), icon='lock', password=True, password_toggle_button=True)
                reg_password_repeat = user_input(_("login_repeat_password"), icon="password", password=True, password_toggle_button=True).on('keydown.enter', handle_register)

                submit_button(text=_("login_make_account"), on_click=handle_register).classes('mt-4')