from nicegui import ui, app

from services import (
    get_user_by_id,
    get_currently_reading_book,
    get_user_by_username,
    are_mutual_friends
)

from views.theme import apply_theme
from views.components import (
    render_header,
    render_mobile_bottom_bar,
    icon_button,
    render_general_stats,
    render_currently_reading,
    render_follow_button
)

@ui.page('/profile')
@ui.page('/profile/{username}')
def profile_page(username: str | None = None) -> None:
    current_user_id = app.storage.user.get('user_id')
    current_user = get_user_by_id(user_id=app.storage.user.get("user_id"))

    if not current_user_id:
        ui.navigate.to('/login')
        return

    apply_theme()

    if username is None or username == current_user.username:
        profile_user = current_user
        is_owner = True
        is_friend = False
    else:
        profile_user = get_user_by_username(username=username)
        is_owner = False
        if profile_user:
            is_friend = are_mutual_friends(current_user_id=current_user.id, target_user_id=profile_user.id)

    render_header(current_path=f'/{'profile' if is_owner else 'search'}')

    if not profile_user:
        ui.label('Usuario not found').classes('text-2xl text-red-500 m-8')
        return

    # UI STARTS HERE

    with ui.column().classes('max-w-7xl w-full mx-auto px-4 md:px-0 py-4 gap-6 items-center pb-28 sm:pb-4'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label(f"@{profile_user.username}").classes("text-3xl text-slate-700 font-bold")

            if is_owner:
                icon_button(icon='settings', color='slate-500', on_click=lambda: ui.notify("Opening settings!", type="positive"), tooltip="Open settings").classes('text-lg')
            else:
                render_follow_button(current_user_id=current_user_id, profile_user_id=profile_user.id)

            ui.separator().classes('w-full')

        can_see_generals_stats = (
            is_owner or
            profile_user.privacy_settings.get("general_stats") == "public" or
            profile_user.privacy_settings.get("general_stats") == "friends" and is_friend
        )

        render_general_stats(user_id=profile_user.id) if can_see_generals_stats else None

        can_see_reading = (
            is_owner or
            profile_user.privacy_settings.get("reading") == "public" or
            profile_user.privacy_settings.get("reading") == "friends" and is_friend
        )

        render_currently_reading(user_id=profile_user.id, currently_reading_book=get_currently_reading_book(user_id=profile_user.id)) if can_see_reading else None


    render_mobile_bottom_bar(current_path='/profile')