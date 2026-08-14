from nicegui import ui
from typing import Callable

from services import (
    is_following,
    follow_user,
    unfollow_user,
    get_follower_count,
    get_following_count,
    are_mutual_friends,
    get_user_by_id
)

from views.components.core import submit_button, icon_button

def render_follow_button(current_user_id: int, target_user_id: int, is_friend: bool, on_change: Callable = None) -> None:
    is_already_following = is_following(current_user_id=current_user_id, target_user_id=target_user_id)
    target_username = get_user_by_id(target_user_id).username

    def handle_follow(already_following: bool) -> None:
        if already_following:
            unfollow_user(current_user_id=current_user_id, target_user_id=target_user_id)
            ui.notify(f'You no longer follow @{target_username}')
        else:
            follow_user(current_user_id=current_user_id, target_user_id=target_user_id)
            ui.notify(f'You now follow @{target_username}!')

        if on_change:
            on_change()
        else:
            follow_button.refresh(already_following=not already_following, is_friend=are_mutual_friends(current_user_id=current_user_id, target_user_id=target_user_id))


    @ui.refreshable
    def follow_button(already_following: bool, is_friend: bool) -> None:
        if is_friend:
            friend_button = (
                submit_button(text="Friends", on_click=lambda: handle_follow(already_following=True))
                .classes(add="hover:!bg-red-500 hover:!text-white transition-colors", remove='w-full')
                .on("mouseenter", lambda: friend_button.set_text("Unfollow"))
                .on("mouseleave", lambda: friend_button.set_text("Friends"))
            )
        elif already_following:
            following_button = (
                submit_button(text="Following", on_click=lambda: handle_follow(already_following=True))
                .classes(add="hover:!bg-red-500 hover:!text-white transition-colors", remove='w-full')
                .on("mouseenter", lambda: following_button.set_text("Unfollow"))
                .on("mouseleave", lambda: following_button.set_text("Following"))
            )
        else:
            submit_button(text="Follow", on_click=lambda: handle_follow(already_following=False)).classes(add="hover:color-slate-500", remove='w-full')

    follow_button(already_following=is_already_following, is_friend=is_friend)

def render_follows(user_id: int, can_see_follows: bool) -> None:
    with ui.row().classes('items-center gap-3 text-slate-600 text-sm ml-1 md:text-base'):
        render_follower_count(user_id=user_id, can_see_follows=can_see_follows)
        ui.label('·').classes('text-slate-300 font-bold select-none')
        render_following_count(user_id=user_id, can_see_follows=can_see_follows)

def render_follower_count(user_id: int, can_see_follows: bool) -> None:
    follower_count = get_follower_count(user_id=user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900' if can_see_follows else ''

    follower_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with follower_count_container:
        ui.label(follower_count).classes(f'text-slate-800 {text_hover} font-bold')
        ui.label("followers").classes(f'text-slate-500 {text_hover}')

    if can_see_follows:
        follower_count_container.on("click", lambda: follow_dialog(user_id=user_id, start_on_followers=True))

def render_following_count(user_id: int, can_see_follows: bool) -> None:
    following_count = get_following_count(user_id=user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900' if can_see_follows else ''

    following_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with following_count_container:
        ui.label(following_count).classes(f'text-slate-800 {text_hover} font-bold')
        ui.label("following").classes(f'text-slate-500 {text_hover}')

    if can_see_follows:
        following_count_container.on("click", lambda: follow_dialog(user_id=user_id, start_on_followers=False))

def follow_dialog(user_id: int, start_on_followers: bool) -> None:
    initial_state = "followers" if start_on_followers else "following"

    with ui.dialog().classes('items-center') as dialog:
        with ui.card().classes('w-full max-w-lg p-6 flex flex-col gap-4 '
            'my-auto max-h-[85vh] rounded-2xl'):

            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label("@user").classes('text-2xl font-bold text-slate-700')
                icon_button(icon="close", color="slate-700", tooltip="Close", on_click=dialog.close)


            @ui.refreshable
            def dynamic_dialog_content(state: str) -> None:
                match state:
                    case "followers":
                        ui.label("followers")
                    case "following":
                        ui.label("following")
                    case "friends":
                        ui.label("friends")

            dynamic_dialog_content(state=initial_state)

    dialog.open()