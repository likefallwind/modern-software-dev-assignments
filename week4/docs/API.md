# API Reference

> Auto-generated from `/openapi.json`. Do not edit manually — run `/docs-sync` to update.

**Title:** Modern Software Dev Starter (Week 4)
**Version:** 0.1.0
**Base URL:** `http://localhost:8000`

---

## Notes

### `GET /notes/`
List all notes.

**Response `200`**
```json
[
  { "id": 1, "title": "string", "content": "string" }
]
```

---

### `POST /notes/`
Create a new note.

**Request body**
```json
{ "title": "string", "content": "string" }
```

> **Validation:** Both `title` and `content` are required and must be non-empty strings (`min_length=1`). Violating this constraint returns `422 Unprocessable Entity`.

**Response `201`**
```json
{ "id": 1, "title": "string", "content": "string" }
```

**Error responses**
| Status | Description                        |
|--------|------------------------------------|
| `422`  | Validation error (empty field)     |

---

### `GET /notes/search/`
Search notes by query string (case-insensitive).

**Query params**
| Name | Type   | Required |
|------|--------|----------|
| `q`  | string | No       |

**Response `200`**
```json
[
  { "id": 1, "title": "string", "content": "string" }
]
```

---

### `GET /notes/{note_id}`
Get a single note by ID.

**Path params**
| Name      | Type    | Required |
|-----------|---------|----------|
| `note_id` | integer | Yes      |

**Response `200`**
```json
{ "id": 1, "title": "string", "content": "string" }
```

**Error responses**
| Status | Description      |
|--------|------------------|
| `404`  | Note not found   |

---

### `PUT /notes/{note_id}`
Update a note's title and/or content. Both fields are optional; only the fields provided will be updated.

**Path params**
| Name      | Type    | Required |
|-----------|---------|----------|
| `note_id` | integer | Yes      |

**Request body**
```json
{ "title": "string", "content": "string" }
```

> Both `title` and `content` are optional. Omit any field you do not want to update.

**Response `200`**
```json
{ "id": 1, "title": "string", "content": "string" }
```

**Error responses**
| Status | Description      |
|--------|------------------|
| `404`  | Note not found   |

---

### `DELETE /notes/{note_id}`
Delete a note by ID.

**Path params**
| Name      | Type    | Required |
|-----------|---------|----------|
| `note_id` | integer | Yes      |

**Response `204`**
No content.

**Error responses**
| Status | Description      |
|--------|------------------|
| `404`  | Note not found   |

---

### `POST /notes/{note_id}/extract`
Extract action items and tags from a note's content using LLM-based extraction.

**Path params**
| Name      | Type    | Required |
|-----------|---------|----------|
| `note_id` | integer | Yes      |

**Response `200`**
```json
{
  "action_items": ["string"],
  "tags": ["string"]
}
```

**Error responses**
| Status | Description      |
|--------|------------------|
| `404`  | Note not found   |

---

## Action Items

### `GET /action-items/`
List all action items.

**Response `200`**
```json
[
  { "id": 1, "description": "string", "completed": false }
]
```

---

### `POST /action-items/`
Create a new action item.

**Request body**
```json
{ "description": "string" }
```

> **Validation:** `description` is required and must be a non-empty string (`min_length=1`). Violating this constraint returns `422 Unprocessable Entity`.

**Response `201`**
```json
{ "id": 1, "description": "string", "completed": false }
```

**Error responses**
| Status | Description                        |
|--------|------------------------------------|
| `422`  | Validation error (empty field)     |

---

### `PUT /action-items/{item_id}/complete`
Mark an action item as completed.

**Path params**
| Name      | Type    | Required |
|-----------|---------|----------|
| `item_id` | integer | Yes      |

**Response `200`**
```json
{ "id": 1, "description": "string", "completed": true }
```

**Error responses**
| Status | Description             |
|--------|-------------------------|
| `404`  | Action item not found   |
