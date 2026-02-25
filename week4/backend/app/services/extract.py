import re


def extract_action_items(text: str) -> dict:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    action_items = [
        line for line in lines if line.endswith("!") or line.lower().startswith("todo:")
    ]
    tags = list({word[1:] for word in re.findall(r"#\w+", text)})
    return {"action_items": action_items, "tags": tags}
