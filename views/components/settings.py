from nicegui import ui

from models import User
from services import update_settings

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

    with ui.column().classes('w-full gap-4 mt-6 pl-4 sm:pl-8'):
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