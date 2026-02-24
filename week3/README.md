# Open Library MCP Server (FastMCP)

This MCP server provides tools to search for books and retrieve metadata from the [Open Library API](https://openlibrary.org/developers/api). It is built using the `FastMCP` framework for a clean and efficient implementation.

## Features

- **Tool: `search_books`**: Search for books by title, author, or keyword.
- **Tool: `get_book_details`**: Fetch detailed information (description, subjects) for a specific book using its Work ID or ISBN.
- **Resilience**: Includes connection timeouts and graceful error handling for API failures.
- **Framework**: Powered by `FastMCP`, providing automatic STDIO transport and error management.

## Prerequisites

- Python 3.10 or higher.
- `pip` and `venv`.

## Setup

1.  Navigate to the `week3/` directory:
    ```bash
    cd week3
    ```
2.  The environment and dependencies are already set up in `week3/venv`. To re-install manually:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install mcp httpx
    ```

## Usage

### Running with MCP Inspector

To test the server locally:
```bash
npx @modelcontextprotocol/inspector week3/venv/bin/python3 week3/server/app.py
```

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "open-library": {
      "command": "/home/likefallwind/code/modern-software-dev-assignments/week3/venv/bin/python3",
      "args": [
        "/home/likefallwind/code/modern-software-dev-assignments/week3/server/app.py"
      ]
    }
  }
}
```

## Tool Reference

### `search_books`
- **Arguments**:
  - `query` (string, required): Search term.
  - `limit` (int, default: 5): Max results.
- **Example**: `search_books(query="The Great Gatsby")`

### `get_book_details`
- **Arguments**:
  - `identifier` (string, required): Work ID (e.g., `OL27448W`) or ISBN.
  - `id_type` (string, default: "work"): `work` or `isbn`.
- **Example**: `get_book_details(identifier="OL27448W")`
