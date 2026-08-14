from nicegui import ui
from typing import Callable

from services import (
    is_following,
    follow_user,
    unfollow_user,
    get_follower_count,
    get_followed_count,
    are_mutual_friends,
    get_user_by_id
)

from views.components.core import submit_button

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