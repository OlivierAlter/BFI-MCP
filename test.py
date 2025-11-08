#!/usr/bin/env python3
"""
Simple test script for BFI-MCP
Tests data loading and filtering without MCP protocol
"""

from data_loader import BFIDataLoader
from filters import FilmFilter

def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def main():
    print_header("BFI-MCP Test Suite")

    # Test 1: Load data
    print("Test 1: Loading data...")
    try:
        loader = BFIDataLoader("./data")
        print(f"✓ Loaded {loader.get_film_count()} films")
        print(f"✓ Total screenings: {loader.get_total_screenings()}")
        print(f"✓ Categories: {', '.join(loader.get_categories())}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    # Test 2: Get all films
    print_header("Test 2: Get all films")
    films = loader.get_all_films()
    print(f"Sample films:")
    for film in films[:3]:
        print(f"  • {film.get('title', 'Unknown')}")
        print(f"    Director: {film.get('director', 'Unknown')}")
        print(f"    Screenings: {len(film.get('screenings', []))}")

    # Test 3: Filter by category
    print_header("Test 3: Filter by category (james_cameron)")
    cameron_films = FilmFilter.filter_films(films, category="james_cameron")
    print(f"Found {len(cameron_films)} films:")
    for film in cameron_films[:5]:
        print(f"  • {film.get('title', 'Unknown')}")

    # Test 4: Filter by location
    print_header("Test 4: Filter by location (BFI IMAX)")
    imax_films = FilmFilter.filter_films(films, location="BFI IMAX")
    print(f"Found {len(imax_films)} films with IMAX screenings:")
    for film in imax_films[:3]:
        print(f"  • {film.get('title', 'Unknown')}")
        for screen in film.get('screenings', []):
            print(f"    {screen.get('date')} at {screen.get('time')}")

    # Test 5: Search
    print_header("Test 5: Search for 'Hitchcock'")
    results = FilmFilter.search_films(films, "Hitchcock")
    print(f"Found {len(results)} films:")
    for film in results[:5]:
        print(f"  • {film.get('title', 'Unknown')}")

    # Test 6: Get single film
    print_header("Test 6: Get film details")
    film = loader.get_film_by_title("The Terminator")
    if film:
        print(f"Title: {film.get('title')}")
        print(f"Director: {film.get('director')}")
        print(f"Runtime: {film.get('runtime')}")
        print(f"Format: {film.get('format')}")
        print(f"Screenings: {len(film.get('screenings', []))}")
        for screen in film.get('screenings', []):
            print(f"  • {screen.get('date')} at {screen.get('time')} ({screen.get('location')})")
    else:
        print("✗ Film not found")

    # Test 7: Filter by date range
    print_header("Test 7: Filter by date range (Oct 24 - Oct 31)")
    dated_films = FilmFilter.filter_films(
        films,
        start_date="2025-10-24",
        end_date="2025-10-31"
    )
    print(f"Found {len(dated_films)} films screening in this period:")
    for film in dated_films[:3]:
        print(f"  • {film.get('title', 'Unknown')}")
        for screen in film.get('screenings', [])[:2]:
            print(f"    {screen.get('date')} at {screen.get('time')}")

    # Test 8: Get locations and directors
    print_header("Test 8: Available metadata")
    locations = FilmFilter.get_locations(films)
    directors = FilmFilter.get_directors(films)
    print(f"Locations: {', '.join(locations)}")
    print(f"\nTop directors (first 10):")
    for director in directors[:10]:
        print(f"  • {director}")

    print_header("All tests completed! ✅")

if __name__ == "__main__":
    main()
