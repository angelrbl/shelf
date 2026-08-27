from nicegui import ui

from models import User, SettingsPrivacy

from services import (
    get_currently_reading_books,
    get_user_by_username,
    are_mutual_friends,
    get_top_shelf,
    get_most_wished
)

from views.i18n import _
from views.components import (
    icon_button,
    render_insights,
    render_currently_reading,
    render_follow_button,
    render_follows,
    render_top_shelf,
    render_most_wished,
    render_user_stats
)

@ui.refreshable
def render_profile_body(current_user: User, requested_username: str | None):
    if requested_username is None or requested_username == current_user.username:
            profile_user = current_user
            is_owner = True
            is_friend = False
    else:
        profile_user = get_user_by_username(username=requested_username)
        is_owner = False
        if profile_user:
            is_friend = are_mutual_friends(current_user_id=current_user.id, target_user_id=profile_user.id)

    if not profile_user:
        with ui.column().classes('w-full items-center justify-center mt-12 pb-28'):
            ui.label(_("profile_user_not_found")).classes('text-2xl text-red-500 font-semibold')
        return

    # UI STARTS HERE

    with ui.column().classes('max-w-7xl w-full mx-auto px-4 md:px-0 py-4 gap-6 items-center pb-28 sm:pb-4'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.column().classes('gap-2'):
                ui.label(f"@{profile_user.username}").classes("text-3xl text-slate-700 dark:text-neutral-200 font-bold")
                can_see_follows = (
                    is_owner or
                    profile_user.privacy_settings.get("follows") == SettingsPrivacy.PUBLIC or
                    (profile_user.privacy_settings.get("follows") == SettingsPrivacy.FRIENDS and is_friend)
                )
                render_follows(
                    profile_user_id=profile_user.id,
                    current_user_id=current_user.id,
                    can_see_follows=can_see_follows
                )

            with ui.row().classes('sm:pt-3 sm:pr-1'):
                if is_owner:
                    icon_button(icon='settings', color='slate-500', dark="neutral-400", on_click=lambda: ui.navigate.to('/settings'), tooltip=_("profile_open_settings")).classes('text-lg')
                else:
                    render_follow_button(
                        current_user_id=current_user.id,
                        target_user_id=profile_user.id,
                        is_friend=is_friend,
                        on_change=render_profile_body.refresh
                    )

        ui.separator().classes('w-full')

        can_see_generals_stats = (
            is_owner or
            profile_user.privacy_settings.get("insights") == SettingsPrivacy.PUBLIC or
            (profile_user.privacy_settings.get("insights") == SettingsPrivacy.FRIENDS and is_friend)
        )

        if can_see_generals_stats:
            render_insights(user_id=profile_user.id)

        can_see_reading = (
            is_owner or
            profile_user.privacy_settings.get("reading") == SettingsPrivacy.PUBLIC or
            (profile_user.privacy_settings.get("reading") == SettingsPrivacy.FRIENDS and is_friend)
        )

        if can_see_reading:
            render_currently_reading(user_id=profile_user.id, currently_reading_books=get_currently_reading_books(user_id=profile_user.id))

        can_see_top_shelf = (
            is_owner or
            profile_user.privacy_settings.get("top_shelf") == SettingsPrivacy.PUBLIC or
            (profile_user.privacy_settings.get("top_shelf") == SettingsPrivacy.FRIENDS and is_friend)
        )

        if can_see_top_shelf:
            render_top_shelf(
                current_user_id=current_user.id,
                profile_user_id=profile_user.id,
                is_owner=is_owner,
                top_shelf=get_top_shelf(user_id=profile_user.id),
            )

        can_see_most_wished = (
            is_owner or
            profile_user.privacy_settings.get("top_wished") == SettingsPrivacy.PUBLIC or
            (profile_user.privacy_settings.get("top_wished") == SettingsPrivacy.FRIENDS and is_friend)
        )

        if can_see_most_wished:
            render_most_wished(
                current_user_id=current_user.id,
                profile_user_id=profile_user.id,
                is_owner=is_owner,
                most_wished_shelf=get_most_wished(user_id=profile_user.id),
            )

        can_see_stats = (
            is_owner or
            profile_user.privacy_settings.get("stats") == SettingsPrivacy.PUBLIC or
            (profile_user.privacy_settings.get("stats") == SettingsPrivacy.FRIENDS and is_friend)
        )

        if can_see_stats:
            render_user_stats(user_id=profile_user.id)