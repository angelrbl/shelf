import pytest

from services.i18n import Translator

@pytest.fixture
def _() -> str:
    translator = Translator()

    def translate(lang: str, key: str, **kwargs):
        return translator.translate(key=key, lang=lang, **kwargs)

    return translate

def test_translation_valid_key(_):
    assert _(lang='en', key='test_key') == 'i am english'

def test_translation_another_language(_):
    assert _(lang='es', key='test_key') == 'soy español'

def test_translation_fallback(_):
    assert _(lang='es', key='test_fallback') == 'i am also english'

def test_translation_invalid_key(_):
    assert _(lang='en', key='test_fallback_2') == "[test_fallback_2]"