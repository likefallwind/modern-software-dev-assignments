import asyncio
import logging
import sys
import urllib.parse
from typing import Any, Dict, List

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# Configure logging to stderr for MCP
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("open-library-mcp")

# MCP Server definition
server = Server("open-library")

# Shared HTTP client with resilience
TIMEOUT = 10.0
BASE_URL = "https://openlibrary.org"

async def fetch_json(client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    """Helper to fetch JSON with error handling."""
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

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="search_books",
            description="Search for books by title, author, or keyword using Open Library.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search term (e.g., 'Lord of the Rings' or 'Tolkien')."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of results to return (default: 5).",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_book_details",
            description="Fetch detailed information about a book using its Open Library Work ID or ISBN.",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "The Work ID (e.g., 'OL27448W') or ISBN (e.g., '9780618640157')."
                    },
                    "id_type": {
                        "type": "string",
                        "enum": ["work", "isbn"],
                        "description": "Type of identifier provided.",
                        "default": "work"
                    }
                },
                "required": ["identifier"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool execution."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        if name == "search_books":
            query = arguments.get("query")
            limit = arguments.get("limit", 5)
            quoted_query = urllib.parse.quote(query)
            url = f"{BASE_URL}/search.json?q={quoted_query}&limit={limit}"
            
            logger.info(f"Searching books with query: {query}")
            data = await fetch_json(client, url)
            
            if "error" in data:
                return [types.TextContent(type="text", text=f"Error: {data['error']}")]
                
            docs = data.get("docs", [])
            if not docs:
                return [types.TextContent(type="text", text="No books found for that query.")]
                
            results = []
            for doc in docs[:limit]:
                title = doc.get("title", "Unknown Title")
                authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
                year = doc.get("first_publish_year", "Unknown Year")
                work_id = doc.get("key", "").split("/")[-1]
                results.append(f"- {title} by {authors} ({year}) [Work ID: {work_id}]")
                
            return [types.TextContent(type="text", text="\n".join(results))]

        elif name == "get_book_details":
            identifier = arguments.get("identifier")
            id_type = arguments.get("id_type", "work")
            
            if id_type == "work":
                url = f"{BASE_URL}/works/{identifier}.json"
            else:
                url = f"{BASE_URL}/isbn/{identifier}.json"
                
            logger.info(f"Fetching details for {id_type}: {identifier}")
            data = await fetch_json(client, url)
            
            if "error" in data:
                return [types.TextContent(type="text", text=f"Error: {data['error']}")]
                
            title = data.get("title", "Unknown Title")
            description = data.get("description", "No description available.")
            if isinstance(description, dict):
                description = description.get("value", "No description available.")
                
            subjects = ", ".join(data.get("subjects", ["None listed"]))[:200]
            
            output = [
                f"Title: {title}",
                f"Description: {description}",
                f"Subjects: {subjects}..." if len(subjects) >= 200 else f"Subjects: {subjects}"
            ]
            
            return [types.TextContent(type="text", text="\n\n".join(output))]

        else:
            raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="open-library",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
