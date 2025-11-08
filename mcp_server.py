"""
BFI-MCP Server
MCP server for accessing BFI film data
"""

import json
import sys
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ToolResult,
)

from data_loader import BFIDataLoader
from filters import FilmFilter

# Initialize server
server = Server("bfi-mcp")

# Global data loader
data_loader: BFIDataLoader | None = None


def initialize_data():
    """Initialize data loader at startup"""
    global data_loader
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        data_dir = script_dir / "data"
        data_loader = BFIDataLoader(str(data_dir))
        print(f"✓ Loaded {data_loader.get_film_count()} films, {data_loader.get_total_screenings()} screenings", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error initializing data: {e}", file=sys.stderr)
        raise


# Define tools
LIST_FILMS_TOOL = Tool(
    name="list-films",
    description="List all BFI films with optional filtering",
    inputSchema={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "Filter by category (e.g., 'james_cameron', 'christmas_films', 'classics')",
            },
            "location": {
                "type": "string",
                "description": "Filter by cinema location (e.g., 'NFT1', 'BFI IMAX', 'NFT2')",
            },
            "director": {
                "type": "string",
                "description": "Filter by director name (partial match)",
            },
            "start_date": {
                "type": "string",
                "description": "Filter screenings from this date (YYYY-MM-DD format)",
            },
            "end_date": {
                "type": "string",
                "description": "Filter screenings until this date (YYYY-MM-DD format)",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of films to return (default: 50)",
            },
        },
    },
)

SEARCH_FILMS_TOOL = Tool(
    name="search-films",
    description="Search for films by title, director, or description",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (searches in title, director, and description)",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 20)",
            },
        },
        "required": ["query"],
    },
)

GET_FILM_DETAILS_TOOL = Tool(
    name="get-film-details",
    description="Get complete details for a specific film",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Film title (must be exact match)",
            },
        },
        "required": ["title"],
    },
)


@server.list_tools()
def list_tools():
    """List available tools"""
    return [LIST_FILMS_TOOL, SEARCH_FILMS_TOOL, GET_FILM_DETAILS_TOOL]


@server.call_tool()
def call_tool(name: str, arguments: dict) -> ToolResult:
    """Handle tool calls"""
    if not data_loader:
        return ToolResult(
            content=[TextContent(type="text", text="Data not initialized")],
            isError=True,
        )

    try:
        if name == "list-films":
            return handle_list_films(arguments)
        elif name == "search-films":
            return handle_search_films(arguments)
        elif name == "get-film-details":
            return handle_get_film_details(arguments)
        else:
            return ToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True,
            )
    except Exception as e:
        return ToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True,
        )


def handle_list_films(arguments: dict) -> ToolResult:
    """Handle list-films tool"""
    category = arguments.get("category")
    location = arguments.get("location")
    director = arguments.get("director")
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")
    limit = arguments.get("limit", 50)

    # Get all films
    films = data_loader.get_all_films()

    # Apply filters
    filtered = FilmFilter.filter_films(
        films,
        category=category,
        location=location,
        director=director,
        start_date=start_date,
        end_date=end_date,
    )

    # Apply limit
    filtered = filtered[:limit]

    # Format response
    if not filtered:
        result = "No films found matching the criteria."
    else:
        lines = [f"Found {len(filtered)} film(s):\n"]
        for film in filtered:
            title = film.get("title", "Unknown")
            director = film.get("director", "Unknown")
            screenings = len(film.get("screenings", []))
            rating = film.get("rating") or "Not rated"
            runtime = film.get("runtime") or "Unknown"

            lines.append(
                f"• {title}\n"
                f"  Director: {director} | Runtime: {runtime} | Rating: {rating}\n"
                f"  Screenings: {screenings}\n"
            )

        result = "\n".join(lines)

    return ToolResult(
        content=[TextContent(type="text", text=result)],
        isError=False,
    )


def handle_search_films(arguments: dict) -> ToolResult:
    """Handle search-films tool"""
    query = arguments.get("query", "").strip()
    limit = arguments.get("limit", 20)

    if not query:
        return ToolResult(
            content=[TextContent(type="text", text="Search query cannot be empty")],
            isError=True,
        )

    # Get all films
    films = data_loader.get_all_films()

    # Search
    results = FilmFilter.search_films(films, query)

    # Apply limit
    results = results[:limit]

    # Format response
    if not results:
        result = f"No films found matching '{query}'."
    else:
        lines = [f"Found {len(results)} film(s) matching '{query}':\n"]
        for film in results:
            title = film.get("title", "Unknown")
            director = film.get("director", "Unknown")
            screenings = len(film.get("screenings", []))

            lines.append(
                f"• {title}\n"
                f"  Director: {director}\n"
                f"  Screenings: {screenings}\n"
            )

        result = "\n".join(lines)

    return ToolResult(
        content=[TextContent(type="text", text=result)],
        isError=False,
    )


def handle_get_film_details(arguments: dict) -> ToolResult:
    """Handle get-film-details tool"""
    title = arguments.get("title", "").strip()

    if not title:
        return ToolResult(
            content=[TextContent(type="text", text="Title cannot be empty")],
            isError=True,
        )

    # Find film
    film = data_loader.get_film_by_title(title)

    if not film:
        return ToolResult(
            content=[TextContent(type="text", text=f"Film '{title}' not found")],
            isError=True,
        )

    # Format response
    lines = []

    # Title and metadata
    lines.append(f"🎬 {film.get('title', 'Unknown')}\n")

    if film.get("country_year"):
        lines.append(f"Country/Year: {film['country_year']}")
    if film.get("director"):
        lines.append(f"Director: {film['director']}")
    if film.get("cast"):
        cast = film['cast']
        if len(cast) > 100:
            cast = cast[:100] + "..."
        lines.append(f"Cast: {cast}")
    if film.get("runtime"):
        lines.append(f"Runtime: {film['runtime']}")
    if film.get("format"):
        lines.append(f"Format: {film['format']}")
    if film.get("rating"):
        lines.append(f"Rating: {film['rating']}")

    lines.append("")

    # Description
    if film.get("description"):
        lines.append(f"Description:\n{film['description']}\n")

    # Screenings
    screenings = film.get("screenings", [])
    if screenings:
        lines.append(f"Screenings ({len(screenings)} total):\n")
        for screening in screenings:
            date = screening.get("date", "Unknown")
            time = screening.get("time", "Unknown")
            location = screening.get("location", "Unknown")
            lines.append(f"  • {date} at {time} ({location})")
    else:
        lines.append("No screenings scheduled.")

    result = "\n".join(lines)

    return ToolResult(
        content=[TextContent(type="text", text=result)],
        isError=False,
    )


def main():
    """Main entry point"""
    initialize_data()
    server.run(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    main()
