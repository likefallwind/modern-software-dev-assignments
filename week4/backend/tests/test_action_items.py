def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_validation_empty_description(client):
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422


def test_complete_action_item_not_found(client):
    r = client.put("/action-items/9999/complete")
    assert r.status_code == 404


def test_list_action_items_empty(client):
    r = client.get("/action-items/")
    assert r.status_code == 200
    assert r.json() == []


def test_list_action_items_multiple(client):
    client.post("/action-items/", json={"description": "First task"})
    client.post("/action-items/", json={"description": "Second task"})
    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    descriptions = [i["description"] for i in items]
    assert "First task" in descriptions
    assert "Second task" in descriptions


def test_complete_item_fields(client):
    r = client.post("/action-items/", json={"description": "Check fields"})
    item_id = r.json()["id"]
    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["id"] == item_id
    assert done["description"] == "Check fields"
    assert done["completed"] is True
