from nicegui import ui
from typing import Callable

from models import User

from services import (
    is_following,
    follow_user,
    unfollow_user,
    get_followers,
    get_following,
    get_friends,
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

def render_follows(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    with ui.row().classes('items-center gap-3 text-slate-600 text-sm ml-1 md:text-base'):
        render_follower_count(profile_user_id=profile_user_id, current_user_id=current_user_id, can_see_follows=can_see_follows)
        ui.label('·').classes('text-slate-300 font-bold select-none')
        render_following_count(profile_user_id=profile_user_id, current_user_id=current_user_id, can_see_follows=can_see_follows)

def render_follower_count(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    follower_count = get_follower_count(user_id=profile_user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900' if can_see_follows else ''

    follower_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with follower_count_container:
        ui.label(follower_count).classes(f'text-slate-800 {text_hover} font-bold')
        ui.label("followers").classes(f'text-slate-500 {text_hover}')

    if can_see_follows:
        follower_count_container.on("click", lambda: follow_dialog(profile_user_id=profile_user_id, current_user_id=current_user_id, start_on_followers=True))

def render_following_count(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    following_count = get_following_count(user_id=profile_user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900' if can_see_follows else ''

    following_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with following_count_container:
        ui.label(following_count).classes(f'text-slate-800 {text_hover} font-bold')
        ui.label("following").classes(f'text-slate-500 {text_hover}')

    if can_see_follows:
        following_count_container.on("click", lambda: follow_dialog(profile_user_id=profile_user_id, current_user_id=current_user_id, start_on_followers=False))

def render_user_list(users: list[User], current_user_id: int, dialog: ui.dialog, on_status_change: Callable) -> None:
    if not users:
        with ui.card().classes('w-full justify-center items-center h-48 sm:h-56 shadow-none'):
            ui.label('Nothing here yet...').classes('w-full text-lg text-center text-slate-500')
    else:
        with ui.scroll_area().classes('w-full flex-grow h-48 sm:h-56'):
            for user in users:
                with ui.row().classes('w-full items-center justify-between p-4 rounded-xl hover:bg-slate-50'):
                    with ui.column().classes("cursor-pointer").on("click", lambda _, u=user: (dialog.close, ui.navigate.to(f'/profile/{u.username}'))):
                        ui.label(f"@{user.username}").classes('text-lg font-bold text-slate-700')
                    if user.id != current_user_id:
                        render_follow_button(
                            current_user_id=current_user_id,
                            target_user_id=user.id,
                            is_friend=are_mutual_friends(current_user_id=current_user_id, target_user_id=user.id),
                            on_change=on_status_change
                        )

def follow_dialog(profile_user_id: int, current_user_id: int, start_on_followers: bool) -> None:
    profile_user = get_user_by_id(user_id=profile_user_id)

    with ui.dialog().classes('items-center').on('keydown.escpae', lambda: dialog.close()) as dialog:
        with ui.card().classes('w-full max-w-lg p-6 flex flex-col gap-4 '
            'my-auto max-h-[85vh] rounded-2xl'):

            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label(f"@{profile_user.username}").classes('text-2xl font-bold text-slate-700')
                icon_button(icon="close", color="slate-700", tooltip="Close", on_click=dialog.close)

            with ui.tabs().classes('w-full text-slate-700') as tabs:
                followers_tab = ui.tab('Followers')
                following_tab = ui.tab('Following')
                friends_tab = ui.tab('Friends')

            initial_tab = followers_tab if start_on_followers else following_tab

            @ui.refreshable
            def dynamic_tab_content(tab_value):
                def handle_update_content(tab_value):
                    dynamic_tab_content.refresh(tab_value=tab_value)

                with ui.tab_panels(tabs, value=tab_value).classes('w-full bg-transparent'):
                    with ui.tab_panel(followers_tab).classes('p-0'):
                        followers = get_followers(user_id=profile_user_id)
                        render_user_list(
                            users=followers,
                            current_user_id=current_user_id,
                            dialog=dialog,
                            on_status_change=lambda: handle_update_content(tab_value=followers_tab)
                        )

                    with ui.tab_panel(following_tab).classes('p-0'):
                        following = get_following(user_id=profile_user_id)
                        render_user_list(
                            users=following,
                            current_user_id=current_user_id,
                            dialog=dialog,
                            on_status_change=lambda: handle_update_content(tab_value=following_tab)
                        )

                    with ui.tab_panel(friends_tab).classes('p-0'):
                        friends = get_friends(user_id=profile_user_id)
                        render_user_list(
                            users=friends,
                            current_user_id=current_user_id,
                            dialog=dialog,
                            on_status_change=lambda: handle_update_content(tab_value=friends_tab)
                        )

            dynamic_tab_content(tab_value=initial_tab)
            
    dialog.open()