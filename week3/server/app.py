import logging
import urllib.parse

import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging
# Note: FastMCP handles logging to stderr by default,
# but we can configure the root logger if needed.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open-library-fastmcp")

# Initialize FastMCP
mcp = FastMCP("open-library")

# Constants
TIMEOUT = 10.0
BASE_URL = "https://openlibrary.org"


async def fetch_json(url: str) -> dict:
    """Helper to fetch JSON with error handling."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            return {"error": f"API returned status {e.response.status_code}"}
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return {"error": f"Connection error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {"error": f"Internal error: {str(e)}"}


@mcp.tool()
async def search_books(query: str, limit: int = 5) -> str:
    """
    Search for books by title, author, or keyword using Open Library.

    Args:
        query: The search term (e.g., 'Lord of the Rings' or 'Tolkien').
        limit: Max number of results to return (default: 5).
    """
    quoted_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/search.json?q={quoted_query}&limit={limit}"

    logger.info(f"Searching books with query: {query}")
    data = await fetch_json(url)

    if "error" in data:
        return f"Error: {data['error']}"

    docs = data.get("docs", [])
    if not docs:
        return "No books found for that query."

    results = []
    for doc in docs[:limit]:
        title = doc.get("title", "Unknown Title")
        authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
        year = doc.get("first_publish_year", "Unknown Year")
        work_id = doc.get("key", "").split("/")[-1]
        results.append(f"- {title} by {authors} ({year}) [Work ID: {work_id}]")

    return "\n".join(results)


@mcp.tool()
async def get_book_details(identifier: str, id_type: str = "work") -> str:
    """
    Fetch detailed information about a book using its Open Library Work ID or ISBN.

    Args:
        identifier: The Work ID (e.g., 'OL27448W') or ISBN (e.g., '9780618640157').
        id_type: Type of identifier provided ('work' or 'isbn').
    """
    if id_type == "work":
        url = f"{BASE_URL}/works/{identifier}.json"
    else:
        url = f"{BASE_URL}/isbn/{identifier}.json"

    logger.info(f"Fetching details for {id_type}: {identifier}")
    data = await fetch_json(url)

    if "error" in data:
        return f"Error: {data['error']}"

    title = data.get("title", "Unknown Title")
    description = data.get("description", "No description available.")
    if isinstance(description, dict):
        description = description.get("value", "No description available.")

    subjects = ", ".join(data.get("subjects", ["None listed"]))[:300]

    output = [
        f"Title: {title}",
        f"Description: {description}",
        f"Subjects: {subjects}..." if len(subjects) >= 300 else f"Subjects: {subjects}",
    ]

    return "\n\n".join(output)


if __name__ == "__main__":
    mcp.run()
