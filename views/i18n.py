from nicegui import app
from services import Translator, DEFAULT_LANG

_translator = Translator()

def _(key: str, **kwargs) -> str:
    lang = app.storage.user.get('lang', DEFAULT_LANG)
    return _translator.translate(key, lang, **kwargs)