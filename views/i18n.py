from nicegui import ui, app
from services import Translator, DEFAULT_LANG

_translator = Translator()

def _(key: str, **kwargs) -> str:
    lang = app.storage.user.get('lang', DEFAULT_LANG)
    return _translator.translate(key=key, lang=lang, **kwargs)

def switch_language(lang: str) -> None:
    if lang == 'en':
        app.storage.user.pop("lang", 'en')
    else:
        app.storage.user["lang"] = lang

    ui.navigate.reload()