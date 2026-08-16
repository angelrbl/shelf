from nicegui import ui, app

from models import User
from services import update_settings, get_user_by_username, update_username, update_password, delete_user

from views.components.core import submit_button, icon_button, user_input

PRIVACY_OPTIONS = {
    'public': 'Public',
    'friends': 'Friends Only',
    'private': 'Private'
}

PRIVACY_LABELS = {
    'follows': 'Who can see my followers and following',
    'general_stats': 'Who can see my general reading stats',
    'reading': 'Who can see what I am currently reading',
    'top_shelf': 'Who can see my top shelf',
    'top_wished': 'Who can see my most wished books',
    'stats': 'Who can see my reading stats'
}

def render_privacy_settings(user: User) -> None:
    current_settings = user.privacy_settings or {}

    with ui.column().classes('w-full gap-4 mt-3 pl-4 sm:pl-8'):
        for settings_key, label_text in PRIVACY_LABELS.items():
            current_value = current_settings.get(settings_key, 'public')

            with ui.row().classes('w-full flex-col sm:flex-row justify-between sm:items-center border-b border-slate-200 py-4 gap-3 sm:gap-0'):
                ui.label(label_text).classes('text-sm sm:text-base text-slate-700 font-medium')

                (
                    ui.select(
                        options=PRIVACY_OPTIONS,
                        value=current_value,
                        on_change=lambda e, key=settings_key, uid=user.id: update_settings(user_id=uid, setting_key=key, new_value=e.value)
                    )
                    .classes('w-full sm:w-40')
                    .props('dense outlined options-dense')
                )

def render_account_settings(user: User) -> None:
    with ui.column().classes('w-full gap-4 sm:mt-3 pl-4 sm:pl-8'):

        render_update_username(user=user)

        with ui.row().classes('w-full flex-col sm:flex-row sm:justify-between sm:items-center border-b border-slate-200 gap-3 py-4 sm:gap-0'):
            ui.label(f"Password: ").classes('pl-4 sm:pl-0 text-sm sm:text-base text-slate-700 font-medium')

            with ui.column().classes('pl-4 sm:pl-0 w-full sm:w-auto gap-2 sm:gap-3 items-start sm:items-end'):
                password = (
                    ui.input(value=f"jajajajajaja", password=True)
                    .props('filled dense input-class="text-slate-800 font-medium" disable')
                )
                (
                    ui.label("Update password")
                    .classes('pl-1 sm:pl-0 sm:pr-2 hover:text-slate-500 text-slate-700 font-bold text-sm cursor-pointer')
                    .on("click", lambda: update_password_dialog(user_id=user.id))
                )

        with ui.row().classes('w-full justify-center mt-2 sm:mt-4'):
            (
                ui.label("Delete account")
                .classes('rounded-xl p-2 text-red-600 text-md hover:bg-red-100 cursor-pointer font-medium')
                .on("click", lambda: delete_user_dialog(user_id=user.id))
            )
            
def render_update_username(user: User) -> None:
    with ui.row().classes('w-full flex-col sm:flex-row sm:justify-between sm:items-center border-b border-slate-200 gap-3 py-4 sm:gap-0'):

        ui.label(f"Username: ").classes('pl-4 sm:pl-0 text-sm sm:text-base text-slate-700 font-medium')
        with ui.row().classes('w-full sm:w-auto flex-row flex-nowrap justify-between items-start gap-3'):
            with ui.column().classes('w-full sm:w-auto gap-1 sm:gap-2 items-start'):
                with ui.row().classes('gap-1 sm:gap-2 items-center flex-nowrap'):
                    ui.label("@").classes('text-sm sm:text-base text-slate-700 font-medium')
                    new_username = (
                        ui.input(value=f"{user.username}")
                        .classes('grow sm:grow-0')
                        .props('filled dense input-class="text-slate-800 font-medium"')
                    )

                @ui.refreshable
                def valid_username_label(hidden: bool = True, valid: bool = True) -> None:
                    if hidden:
                        return

                    if valid:
                        with ui.row().classes(f'items-center gap-1 pl-5 sm:pl-7'):
                            ui.icon("check").classes('text-green-700 font-bold')
                            ui.label("Valid username").classes('text-green-700 font-bold')
                    else:
                        with ui.row().classes(f'items-center gap-1 pl-5 sm:pl-7'):
                            ui.icon("clear").classes('text-red-700 font-bold')
                            ui.label("Username already taken").classes('text-red-700 font-bold')

                valid_username_label(hidden=True)

            @ui.refreshable
            def update_button(hidden: bool):
                if hidden:
                    return
                
                (
                    submit_button(text="Update", on_click=lambda _, uid=user.id: handle_update_username(user_id=uid, new_username=new_username.value))
                    .classes(remove="w-full")
                )

            update_button(hidden=True)

            new_username.on("blur", lambda _, current_username=user.username: handle_check_username(current_username=current_username, username_input=new_username))
            new_username.on("keydown.enter", lambda _, current_username=user.username: handle_check_username(current_username=current_username, username_input=new_username))

        def handle_check_username(current_username: str, username_input: str) -> None:
            username = username_input.value

            if not username:
                username_input.set_value(current_username)
                valid_username_label.refresh(hidden=True)
                update_button.refresh(hidden=True)
                return

            if current_username == username:
                valid_username_label.refresh(hidden=True)
                update_button.refresh(hidden=True)
                return

            user = get_user_by_username(username=username)
            valid_username_label.refresh(hidden=False, valid=(False if user else True))
            update_button.refresh(hidden=(True if user else False))

        def handle_update_username(user_id: int, new_username: str) -> None:
            if user.username == new_username:
                return

            try:
                update_username(user_id=user_id, new_username=new_username)
                ui.notify("Username updated successfully!", type="positive")
                valid_username_label.refresh(hidden=True)
                update_button.refresh(hidden=True)
            except ValueError as e:
                ui.notify(str(e), type="negative")

def update_password_dialog(user_id: int):
    with ui.dialog().classes('items-center').on('keydown.escape', lambda: dialog.close()) as dialog:
        with ui.card().classes('w-full max-w-lg p-6 sm:p-8 flex flex-col '
            'my-auto max-h-[85vh] rounded-2xl'):

            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label(f"Update password").classes('text-2xl font-bold text-slate-700')
                icon_button(icon="close", color="slate-700", tooltip="Close", on_click=dialog.close)

            with ui.column().classes('w-full gap-4 sm:gap-6 justify-between'):
                    current_password = user_input('Current password', icon='password', password=True, password_toggle_button=True)
                    current_password_repeat = user_input('Repeat current password', icon='lock_open', password=True, password_toggle_button=True).classes('mb-2 sm:mb-4')
                    new_password = user_input('New password', icon='lock', password=True, password_toggle_button=True)

                    submit_button(
                        text="Update password",
                        on_click=lambda: handle_update_password(user_id, current_password.value, current_password_repeat.value, new_password.value)
                    )

            def handle_update_password(user_id: int, current_password: str, current_password_repeat: str, new_password: str) -> None:
                if current_password != current_password_repeat:
                    ui.notify('Passwords given do not match.', color='warning')
                    return

                try:
                    update_password(user_id=user_id, new_password=new_password)
                    ui.notify("Password updated successfully!", type="positive")
                    dialog.close()
                except ValueError as e:
                    ui.notify(str(e), type="negative")
                
    dialog.open()

def delete_user_dialog(user_id: int):
    with ui.dialog().classes('items-center').on('keydown.escape', lambda: dialog.close()) as dialog:
        with ui.card().classes('w-full max-w-lg p-6 sm:p-8 flex flex-col '
            'my-auto max-h-[85vh] rounded-2xl'):

            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label(f"Delete account").classes('text-2xl font-bold text-slate-700')
                icon_button(icon="close", color="slate-700", tooltip="Close", on_click=dialog.close)

            with ui.column().classes('w-full gap-4 sm:gap-6 justify-between'):
                    password = user_input('Current password', icon='lock', password=True, password_toggle_button=True)
                    password_repeat = user_input('Repeat current password', icon='password', password=True, password_toggle_button=True).classes('mb-2 sm:mb-4')

                    submit_button(
                        text="Delete",
                        on_click=lambda: handle_delete_user(user_id, password.value, password_repeat.value)
                    ).props('color=red-700')

            def handle_delete_user(user_id: int, password: str, password_repeat: str) -> None:
                if password != password_repeat:
                    ui.notify('Passwords given do not match.', color='warning')
                    return

                try:
                    delete_user(user_id=user_id, password=password)
                    app.storage.clear()
                    ui.notify("Account deleted successfully! Bye!", type="positive")
                    dialog.close()
                    ui.navigate.to('/')
                except ValueError as e:
                    ui.notify(str(e), type="negative")
                
                
    dialog.open()