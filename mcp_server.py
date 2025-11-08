"""
BFI-MCP Server - HTTP/Streamable HTTP Transport
MCP server for accessing BFI film data via HTTP
"""

from pathlib import Path
from typing import Optional
from pydantic import Field

from mcp.server.fastmcp import FastMCP

from data_loader import BFIDataLoader
from filters import FilmFilter

# Initialize FastMCP server with HTTP transport
mcp = FastMCP("bfi-mcp", stateless_http=True)

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
        print(f"✓ Loaded {data_loader.get_film_count()} films, {data_loader.get_total_screenings()} screenings")
    except Exception as e:
        print(f"✗ Error initializing data: {e}")
        raise


# Tool 1: List Films
@mcp.tool()
def list_films(
    category: Optional[str] = Field(None, description="Filter by category (e.g., 'james_cameron', 'christmas_films')"),
    location: Optional[str] = Field(None, description="Filter by cinema location (e.g., 'NFT1', 'BFI IMAX')"),
    director: Optional[str] = Field(None, description="Filter by director name (partial match)"),
    start_date: Optional[str] = Field(None, description="Filter screenings from date (YYYY-MM-DD)"),
    end_date: Optional[str] = Field(None, description="Filter screenings until date (YYYY-MM-DD)"),
    limit: int = Field(50, description="Maximum number of films to return"),
) -> str:
    """List all BFI films with optional filtering"""
    if not data_loader:
        return "Error: Data not initialized"

    try:
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
    except Exception as e:
        return f"Error: {str(e)}"


# Tool 2: Search Films
@mcp.tool()
def search_films(
    query: str = Field(..., description="Search query (searches in title, director, description)"),
    limit: int = Field(20, description="Maximum number of results to return"),
) -> str:
    """Search for films by title, director, or description"""
    if not data_loader:
        return "Error: Data not initialized"

    if not query.strip():
        return "Error: Search query cannot be empty"

    try:
        # Get all films
        films = data_loader.get_all_films()

        # Search
        results = FilmFilter.search_films(films, query)

        # Apply limit
        results = results[:limit]

        # Format response
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
    except Exception as e:
        return f"Error: {str(e)}"


# Tool 3: Get Film Details
@mcp.tool()
def get_film_details(
    title: str = Field(..., description="Film title (exact match)"),
) -> str:
    """Get complete details for a specific film"""
    if not data_loader:
        return "Error: Data not initialized"

    if not title.strip():
        return "Error: Title cannot be empty"

    try:
        # Find film
        film = data_loader.get_film_by_title(title)

        if not film:
            return f"Film '{title}' not found"

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

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main entry point - starts HTTP server"""
    initialize_data()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
