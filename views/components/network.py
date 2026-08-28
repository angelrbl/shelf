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
    get_user_by_id,
    filter_users
)

from views.i18n import _
from views.components.core import submit_button, icon_button, user_input

def render_follow_button(current_user_id: int, target_user_id: int, is_friend: bool, on_change: Callable = None) -> None:
    is_already_following = is_following(current_user_id=current_user_id, target_user_id=target_user_id)
    target_username = get_user_by_id(target_user_id).username

    def handle_follow(already_following: bool) -> None:
        if already_following:
            unfollow_user(current_user_id=current_user_id, target_user_id=target_user_id)
            ui.notify(_("network_no_longer_follow", target_username=target_username))
        else:
            follow_user(current_user_id=current_user_id, target_user_id=target_user_id)
            ui.notify(_("network_now_follow", target_username=target_username))

        if on_change:
            on_change()
        else:
            follow_button.refresh(already_following=not already_following, is_friend=are_mutual_friends(current_user_id=current_user_id, target_user_id=target_user_id))


    @ui.refreshable
    def follow_button(already_following: bool, is_friend: bool) -> None:
        if is_friend:
            friend_button = (
                submit_button(text=_("network_friends"), on_click=lambda: handle_follow(already_following=True))
                .classes(add="hover:!bg-red-500 hover:!text-white transition-colors", remove='w-full')
                .on("mouseenter", lambda: friend_button.set_text(_("network_unfollow")))
                .on("mouseleave", lambda: friend_button.set_text(_("network_friends")))
            )
        elif already_following:
            following_button = (
                submit_button(text=_("network_following"), on_click=lambda: handle_follow(already_following=True))
                .classes(add="hover:!bg-red-500 hover:!text-white transition-colors", remove='w-full')
                .on("mouseenter", lambda: following_button.set_text(_("network_unfollow")))
                .on("mouseleave", lambda: following_button.set_text(_("network_following")))
            )
        else:
            submit_button(text=_("network_follow"), on_click=lambda: handle_follow(already_following=False)).classes(add="hover:color-slate-500 hover:color-neutral-400", remove='w-full')

    follow_button(already_following=is_already_following, is_friend=is_friend)

def render_follows(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    with ui.row().classes('items-center gap-3 text-slate-600 dark:text-neutral-300 text-sm ml-1 md:text-base'):
        render_follower_count(profile_user_id=profile_user_id, current_user_id=current_user_id, can_see_follows=can_see_follows)
        ui.label('·').classes('text-slate-300 dark:text-neutral-600 font-bold select-none')
        render_following_count(profile_user_id=profile_user_id, current_user_id=current_user_id, can_see_follows=can_see_follows)

def render_follower_count(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    follower_count = get_follower_count(user_id=profile_user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900 dark:group-hover:text-neutral-50' if can_see_follows else ''

    follower_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with follower_count_container:
        ui.label(follower_count).classes(f'text-slate-800 dark:text-neutral-100 {text_hover} font-bold')
        ui.label(_("network_follower_count")).classes(f'text-slate-500 dark:text-neutral-400 {text_hover}')

    if can_see_follows:
        follower_count_container.on("click", lambda: follow_dialog(profile_user_id=profile_user_id, current_user_id=current_user_id, start_on_followers=True))

def render_following_count(profile_user_id: int, current_user_id: int, can_see_follows: bool) -> None:
    following_count = get_following_count(user_id=profile_user_id)

    hover_classes = 'cursor-pointer group' if can_see_follows else 'cursor-default'
    text_hover = 'group-hover:text-slate-900 dark:group-hover:text-neutral-50' if can_see_follows else ''

    following_count_container = ui.row().classes(f'items-center gap-1 transition-colors {hover_classes}')

    with following_count_container:
        ui.label(following_count).classes(f'text-slate-800 dark:text-neutral-100 {text_hover} font-bold')
        ui.label(_("network_following_count")).classes(f'text-slate-500 dark:text-neutral-400 {text_hover}')

    if can_see_follows:
        following_count_container.on("click", lambda: follow_dialog(profile_user_id=profile_user_id, current_user_id=current_user_id, start_on_followers=False))

def render_user_list(users: list[User], current_user_id: int, dialog: ui.dialog, on_status_change: Callable) -> None:
    if not users:
        with ui.card().classes('w-full justify-center items-center h-48 sm:h-56 shadow-none'):
            ui.label(_("network_empty")).classes('w-full text-lg text-center text-slate-500 dark:text-neutral-400')
    else:
        def handle_filter_users(users: list[User], query: str | None = None):
            filtered_users = filter_users(users=users, query=query)
            user_list.refresh(users=filtered_users)

        with ui.row().classes('w-full items-center justify-between'):
            query = (
                user_input(label=_("network_search_users"), icon="search")
                .on('keydown.enter', lambda: handle_filter_users(users=users, query=query.value))
                .on('blur', lambda: handle_filter_users(users=users, query=query.value))
                .classes("sm:flex-1")
                .props(remove="outlined", add="clearable")
            )

        @ui.refreshable
        def user_list(users: list[User]):
            with ui.scroll_area().classes('w-full flex-grow h-48 sm:h-56'):
                for user in users:
                    with ui.row().classes('w-full items-center justify-between p-4 rounded-xl group hover:bg-slate-50 dark:hover:bg-neutral-900'):
                        with ui.column().classes("cursor-pointer").on("click", lambda _, u=user: (dialog.close(), ui.navigate.to(f'/profile/{u.username}'))):
                            ui.label(f"@{user.username}").classes('group-hover:text-slate-900 dark:group-hover:text-neutral-50 text-xl font-bold text-slate-700 dark:text-neutral-200')
                        if user.id != current_user_id:
                            render_follow_button(
                                current_user_id=current_user_id,
                                target_user_id=user.id,
                                is_friend=are_mutual_friends(current_user_id=current_user_id, target_user_id=user.id),
                                on_change=on_status_change
                            )

        user_list(users=users)

def follow_dialog(profile_user_id: int, current_user_id: int, start_on_followers: bool) -> None:
    profile_user = get_user_by_id(user_id=profile_user_id)

    with ui.dialog().classes('items-center').on('keydown.escape', lambda: dialog.close()) as dialog:
        with ui.card().classes('w-full max-w-lg p-6 flex flex-col '
            'my-auto max-h-[85vh] rounded-2xl'):

            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label(f"@{profile_user.username}").classes('text-2xl font-bold text-slate-700 dark:text-neutral-200')
                icon_button(icon="close", color="slate-700", dark="neutral-200", tooltip=_("dialog_close_tooltip"), on_click=dialog.close)

            with ui.tabs().classes('w-full text-slate-700 dark:text-neutral-200') as tabs:
                followers_tab = ui.tab(_("network_followers"))
                following_tab = ui.tab(_("network_following"))
                friends_tab = ui.tab(_("network_friends"))

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

@ui.refreshable
def render_search_users(users: list[User], user_id: int) -> None:
    if not users:
        return

    with ui.column().classes('w-full mt-4 sm:mb-2 gap-3 ml-10 pr-20'):
        ui.label(_("network_users")).classes('text-xl font-bold text-slate-700 dark:text-neutral-200 pl-2')

        with ui.row().classes('w-full overflow-x-auto flex-nowrap gap-4 md:gap-6 pb-4 snap-x p-0 items-stretch'):
            for user in users:
                with ui.card().classes(
                    'w-32 sm:w-48 flex-shrink-0 flex flex-col justify-between items-center '
                    'p-4 snap-center shadow-sm rounded-2xl gap-2'):

                    (
                        ui.label(f"@{user.username}")
                        .classes('font-bold text-slate-700 dark:text-neutral-200 cursor-pointer truncate w-full '
                        'text-center text-md sm:text-lg hover:text-slate-900 dark:hover:text-neutral-50')
                        .on('click', lambda _, u=user: ui.navigate.to(f'/profile/{u.username}'))
                    )
                    with ui.row().classes('w-full justify-center scale-90 sm:scale-100'):
                        if user.id != user_id:
                            render_follow_button(
                                current_user_id=user_id,
                                target_user_id=user.id,
                                is_friend=are_mutual_friends(current_user_id=user_id, target_user_id=user.id),
                                on_change=None
                            )
                        else:
                            ui.label("").classes('h-8')