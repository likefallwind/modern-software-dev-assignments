import os
import pytest
from unittest.mock import patch, MagicMock

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
    # Strengthen assertions: check for exact matches and expected count
    expected = [
        "Set up database",
        "implement API extract endpoint",
        "Write tests"
    ]
    assert items == expected


def test_extract_simple_bullets():
    text = """
    - go
    - re
    - eat
    * gg
    """.strip()

    items = extract_action_items(text)
    assert isinstance(items, list)
    assert items == ["go", "re", "eat", "gg"]


def test_extract_deduplication():
    # Test that duplicates are removed while preserving order (case-insensitive)
    text = """
    - Task A
    - Task B
    - task a
    - TASK B
    - Task C
    """.strip()
    
    items = extract_action_items(text)
    assert items == ["Task A", "Task B", "Task C"]


def test_extract_imperative_fallback():
    # Test heuristic fallback for sentences starting with imperative verbs
    # The current crude heuristic requires the sentence to START with the verb
    text = "Implement the new feature. Update the documentation."
    items = extract_action_items(text)
    assert "Implement the new feature." in items
    assert "Update the documentation." in items


def test_extract_action_items_llm_empty_input():
    items = extract_action_items_llm("")
    assert items == []


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_returns_list(mock_chat):
    # Mock LLM response
    mock_response = MagicMock()
    mock_response.message.content = ["Buy groceries", "Finish the report"]
    mock_chat.return_value = mock_response

    text = "Meeting notes: - Buy groceries * Finish the report"
    items = extract_action_items_llm(text)
    
    assert isinstance(items, list)
    assert items == ["Buy groceries", "Finish the report"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_handles_json_string(mock_chat):
    # Mock LLM response returning JSON string instead of list
    mock_response = MagicMock()
    mock_response.message.content = '["Review PR", "Deploy"]'
    mock_chat.return_value = mock_response

    items = extract_action_items_llm("Todo: Review PR, Deploy")
    assert items == ["Review PR", "Deploy"]


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_error_handling(mock_chat):
    # Mock LLM exception
    mock_chat.side_effect = Exception("LLM connection failed")

    items = extract_action_items_llm("Do something")
    assert items == []
