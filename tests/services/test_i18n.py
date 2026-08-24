import pytest

from services.i18n import _, switch_lang

def test_valid_key():
    assert _("test_key") == "i am english"

def test_invalid_key():
    assert _("test_key1") == "[test_key1]"

def test_switch_language_valid():
    assert _("test_key") == "i am english"

    switch_lang(new_lang='es')

    assert _("test_key") == "soy español"

def test_switch_language_invalid():
    with pytest.raises(ValueError):
        switch_lang(new_lang="jp")