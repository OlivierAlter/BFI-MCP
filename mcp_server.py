"""
BFI-MCP Server
MCP server for accessing BFI Southbank film screenings data
"""

from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from data_loader import BFIDataLoader
from filters import FilmFilter

# Initialize FastMCP server
mcp = FastMCP("bfi-mcp", stateless_http=True)

# Load data at startup
_data_loader: BFIDataLoader | None = None


def _load_data() -> BFIDataLoader:
    """Load film data"""
    global _data_loader
    if _data_loader is None:
        script_dir = Path(__file__).parent
        data_dir = script_dir / "data"
        _data_loader = BFIDataLoader(str(data_dir))
        print(f"✓ Loaded {_data_loader.get_film_count()} films, {_data_loader.get_total_screenings()} screenings")
    return _data_loader


@mcp.tool(
    title="List Films",
    description="List all BFI films with optional filtering",
)
def list_films(
    category: Optional[str] = Field(None, description="Filter by category (e.g., 'james_cameron', 'christmas_films', 'classics')"),
    location: Optional[str] = Field(None, description="Filter by cinema location (e.g., 'NFT1', 'BFI IMAX')"),
    director: Optional[str] = Field(None, description="Filter by director name (partial match)"),
    start_date: Optional[str] = Field(None, description="Filter screenings from date (YYYY-MM-DD)"),
    end_date: Optional[str] = Field(None, description="Filter screenings until date (YYYY-MM-DD)"),
    limit: int = Field(50, description="Maximum number of films to return"),
) -> str:
    """List all BFI films with optional filtering by category, location, director, or date range"""
    loader = _load_data()
    films = loader.get_all_films()

    filtered = FilmFilter.filter_films(
        films,
        category=category,
        location=location,
        director=director,
        start_date=start_date,
        end_date=end_date,
    )

    filtered = filtered[:limit]

    if not filtered:
        return "No films found matching the criteria."

    lines = [f"Found {len(filtered)} film(s):\n"]
    for film in filtered:
        title = film.get("title", "Unknown")
        director_name = film.get("director", "Unknown")
        screenings = len(film.get("screenings", []))
        rating = film.get("rating") or "Not rated"
        runtime = film.get("runtime") or "Unknown"

        lines.append(
            f"• {title}\n"
            f"  Director: {director_name} | Runtime: {runtime} | Rating: {rating}\n"
            f"  Screenings: {screenings}\n"
        )

    return "\n".join(lines)


@mcp.tool(
    title="Search Films",
    description="Search for films by title, director, or description",
)
def search_films(
    query: str = Field(..., description="Search query"),
    limit: int = Field(20, description="Maximum number of results to return"),
) -> str:
    """Search for films by title, director, or description"""
    if not query.strip():
        return "Error: Search query cannot be empty"

    loader = _load_data()
    films = loader.get_all_films()
    results = FilmFilter.search_films(films, query)
    results = results[:limit]

    if not results:
        return f"No films found matching '{query}'."

    lines = [f"Found {len(results)} film(s) matching '{query}':\n"]
    for film in results:
        title = film.get("title", "Unknown")
        director_name = film.get("director", "Unknown")
        screenings = len(film.get("screenings", []))

        lines.append(
            f"• {title}\n"
            f"  Director: {director_name}\n"
            f"  Screenings: {screenings}\n"
        )

    return "\n".join(lines)


@mcp.tool(
    title="Get Film Details",
    description="Get complete details for a specific film",
)
def get_film_details(
    title: str = Field(..., description="Film title (exact match)"),
) -> str:
    """Get complete details for a specific film including screenings and metadata"""
    if not title.strip():
        return "Error: Title cannot be empty"

    loader = _load_data()
    film = loader.get_film_by_title(title)

    if not film:
        return f"Film '{title}' not found"

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

    return "\n".join(lines)


if __name__ == "__main__":
    import os
    _load_data()
    # Lambda expects server on port 8080, bind to 0.0.0.0 for container access
    # FastMCP reads HOST and PORT from environment variables
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", "8080")
    mcp.run(transport="streamable-http")
