import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_bullet_list():
    text = """
    Meeting notes:
    - Buy groceries
    * Finish the report
    1. Call client
    - Schedule team meeting
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0
    assert any("groceries" in item.lower() for item in items)


def test_extract_action_items_llm_keyword_prefixed():
    text = """
    Todo: Review pull request
    Action: Update documentation
    Next: Deploy to production
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3


def test_extract_action_items_llm_empty_input():
    text = ""

    items = extract_action_items_llm(text)
    assert items == []


def test_extract_action_items_llm_regular_text():
    text = """
    The project deadline is next Friday. We need to finish the API endpoint.
    John will send the email. Sarah needs to review the code.
    Remember to buy milk on the way home.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)


def test_extract_action_items_llm_simple_bullets():
    text = """
    - go
    - re
    - eat
    * gg
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0
