from nicegui import ui, app

from services import get_user_by_id

from views.theme import apply_theme
from views.components import render_header, render_mobile_bottom_bar, render_profile_body

@ui.page('/profile')
@ui.page('/profile/{username}')
def profile_page(username: str | None = None) -> None:
    current_user_id = app.storage.user.get('user_id')
    current_user = get_user_by_id(current_user_id)

    if not current_user_id or not current_user:
        ui.navigate.to('/login')
        return

    apply_theme()

    is_my_profile = username is None or username == current_user.username
    render_header(current_path=f'/{'profile' if is_my_profile else 'search'}')

    render_profile_body(current_user=current_user, requested_username=username)
    
    render_mobile_bottom_bar(current_path=f'/{'profile' if is_my_profile else 'search'}')