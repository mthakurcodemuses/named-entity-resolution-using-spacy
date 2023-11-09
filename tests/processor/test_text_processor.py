import pytest

from app.processor.text_processor import TextProcessor


@pytest.fixture(scope='function')
def text_processor():
    return TextProcessor()


def test_get_entities_person_entity(text_processor):
    entities_holder = text_processor.get_entities('Hello, John!')
    assert len(entities_holder['entities']) == 1


def test_get_entities_excluded_entity(text_processor):
    entities_holder = text_processor.get_entities('Show me the dollars!')
    assert len(entities_holder['entities']) == 0


def test_get_entities(text_processor):
    assert text_processor.get_entities('Hello, John!')
