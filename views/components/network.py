from nicegui import ui

from views.components.core import submit_button

def render_follow_button(current_user_id: int, profile_user_id: int) -> None:
    already_following = False

    @ui.refreshable
    def follow_button(is_following: bool) -> None:
        if is_following:
            submit_button(text="Following", on_click=lambda: ui.notify("Stopped following")).classes(remove='w-full')
        else:
            submit_button(text="Follow", on_click=lambda: ui.notify("Started following")).classes(remove='w-full')

    follow_button(is_following=already_following)