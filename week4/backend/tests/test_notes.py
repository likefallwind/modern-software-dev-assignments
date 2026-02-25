def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_case_insensitive(client):
    client.post("/notes/", json={"title": "CaseTest", "content": "Unique content here"})
    r = client.get("/notes/search/", params={"q": "unique"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note(client):
    r = client.post("/notes/", json={"title": "Old Title", "content": "Old content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "New Title"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "Old content"


def test_update_note_not_found(client):
    r = client.put("/notes/9999", json={"title": "X"})
    assert r.status_code == 404


def test_delete_note(client):
    r = client.post("/notes/", json={"title": "To Delete", "content": "bye"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/9999")
    assert r.status_code == 404


def test_extract_endpoint(client):
    r = client.post("/notes/", json={"title": "Extract", "content": "TODO: do something #work"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract")
    assert r.status_code == 200
    data = r.json()
    assert "action_items" in data
    assert "tags" in data
    assert "work" in data["tags"]


def test_extract_endpoint_not_found(client):
    r = client.post("/notes/9999/extract")
    assert r.status_code == 404


def test_validation_empty_title(client):
    r = client.post("/notes/", json={"title": "", "content": "Some content"})
    assert r.status_code == 422


def test_validation_empty_content(client):
    r = client.post("/notes/", json={"title": "Title", "content": ""})
    assert r.status_code == 422


def test_get_note_by_id(client):
    r = client.post("/notes/", json={"title": "Fetch Me", "content": "Specific content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Fetch Me"
    assert data["content"] == "Specific content"


def test_get_note_by_id_not_found(client):
    r = client.get("/notes/9999")
    assert r.status_code == 404


def test_update_note_only_content(client):
    r = client.post("/notes/", json={"title": "Keep Title", "content": "Old content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"content": "New content"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Keep Title"
    assert data["content"] == "New content"


def test_update_note_both_fields(client):
    r = client.post("/notes/", json={"title": "Old Title", "content": "Old content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "New Title", "content": "New content"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New content"


def test_search_empty_q_returns_all(client):
    client.post("/notes/", json={"title": "Alpha", "content": "First note"})
    client.post("/notes/", json={"title": "Beta", "content": "Second note"})

    r = client.get("/notes/search/", params={"q": ""})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 2


def test_search_no_match_returns_empty(client):
    client.post("/notes/", json={"title": "Regular", "content": "Nothing special"})

    r = client.get("/notes/search/", params={"q": "zzz_no_match_xyz"})
    assert r.status_code == 200
    items = r.json()
    assert items == []


def test_search_matches_title(client):
    client.post("/notes/", json={"title": "UniqueTitle123", "content": "Generic content"})

    r = client.get("/notes/search/", params={"q": "uniquetitle123"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(n["title"] == "UniqueTitle123" for n in items)


def test_search_matches_content(client):
    client.post("/notes/", json={"title": "Irrelevant", "content": "UniqueContent456"})

    r = client.get("/notes/search/", params={"q": "uniquecontent456"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(n["content"] == "UniqueContent456" for n in items)


def test_delete_note_makes_it_unfetchable(client):
    r = client.post("/notes/", json={"title": "Temporary", "content": "Will be gone"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_extract_returns_empty_lists_for_plain_text(client):
    r = client.post("/notes/", json={"title": "Plain", "content": "Nothing special here"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract")
    assert r.status_code == 200
    data = r.json()
    assert data["action_items"] == []
    assert data["tags"] == []
