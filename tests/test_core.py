import pytest

from brand_manager.core import DemoProvider, DraftStore


def test_demo_selection_and_profile():
    provider = DemoProvider()
    assert provider.list_brands()[0]["id"] == "demo-brand"
    assert provider.list_locations("demo-brand")[0]["id"] == "demo-location"
    assert provider.get_profile("demo-location")["source"] == "demo"


def test_publish_requires_explicit_confirmation_and_is_single_use():
    store = DraftStore()
    draft = store.create("loc", "Hello", None)
    with pytest.raises(ValueError):
        store.confirm(draft["confirmation_token"], False)
    assert store.confirm(draft["confirmation_token"], True)["text"] == "Hello"
    with pytest.raises(ValueError):
        store.confirm(draft["confirmation_token"], True)

