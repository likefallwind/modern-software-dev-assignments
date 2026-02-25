from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    result = extract_action_items(text)
    assert "TODO: write tests" in result["action_items"]
    assert "Ship it!" in result["action_items"]


def test_extract_tags():
    text = "Fix the bug #bugfix and deploy #release #bugfix"
    result = extract_action_items(text)
    assert set(result["tags"]) == {"bugfix", "release"}


def test_extract_no_tags():
    text = "No tags here"
    result = extract_action_items(text)
    assert result["tags"] == []


def test_extract_empty_text():
    result = extract_action_items("")
    assert result["action_items"] == []
    assert result["tags"] == []


def test_extract_no_action_items():
    text = "Just a regular sentence with no tasks."
    result = extract_action_items(text)
    assert result["action_items"] == []


def test_extract_action_item_exclamation():
    text = "Do the laundry!"
    result = extract_action_items(text)
    assert "Do the laundry!" in result["action_items"]


def test_extract_action_item_todo_case_insensitive():
    text = "TODO: finish the report"
    result = extract_action_items(text)
    assert "TODO: finish the report" in result["action_items"]


def test_extract_returns_dict_keys():
    result = extract_action_items("some text")
    assert "action_items" in result
    assert "tags" in result


def test_extract_multiple_tags():
    text = "Meeting notes #team #planning #q1"
    result = extract_action_items(text)
    assert set(result["tags"]) == {"team", "planning", "q1"}
