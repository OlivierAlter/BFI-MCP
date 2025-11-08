"""
BFI-MCP Filters
Filtering and searching logic for films
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

class FilmFilter:
    """Applies filters to films"""

    @staticmethod
    def filter_films(
        films: List[Dict[str, Any]],
        category: Optional[str] = None,
        location: Optional[str] = None,
        director: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter films based on multiple criteria

        Args:
            films: List of films to filter
            category: Film category (e.g., "james_cameron", "christmas_films")
            location: Cinema location (e.g., "NFT1", "BFI IMAX")
            director: Director name (partial match)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Filtered list of films
        """
        results = films.copy()

        # Filter by category
        if category:
            results = [f for f in results if f.get('category', '') == category.lower()]

        # Filter by director (partial match)
        if director:
            director_lower = director.lower()
            results = [
                f for f in results
                if director_lower in (f.get('director', '') or '').lower()
            ]

        # Filter by location and date range
        if location or start_date or end_date:
            results = FilmFilter._filter_by_screenings(
                results, location, start_date, end_date
            )

        return results

    @staticmethod
    def _filter_by_screenings(
        films: List[Dict[str, Any]],
        location: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Filter films that have screenings matching the criteria"""
        results = []

        for film in films:
            screenings = film.get('screenings', [])
            if not screenings:
                continue

            # Filter screenings
            matching_screenings = screenings.copy()

            # Filter by location
            if location:
                matching_screenings = [
                    s for s in matching_screenings
                    if s.get('location', '').upper() == location.upper()
                ]

            # Filter by date range
            if start_date or end_date:
                matching_screenings = FilmFilter._filter_by_date_range(
                    matching_screenings, start_date, end_date
                )

            # Only include film if it has matching screenings
            if matching_screenings:
                # Create a copy with filtered screenings
                film_copy = film.copy()
                film_copy['screenings'] = matching_screenings
                results.append(film_copy)

        return results

    @staticmethod
    def _filter_by_date_range(
        screenings: List[Dict[str, str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Filter screenings by date range"""
        results = screenings.copy()

        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                results = [
                    s for s in results
                    if datetime.strptime(s.get('date', ''), '%Y-%m-%d') >= start
                ]
            except ValueError:
                pass

        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                results = [
                    s for s in results
                    if datetime.strptime(s.get('date', ''), '%Y-%m-%d') <= end
                ]
            except ValueError:
                pass

        return results

    @staticmethod
    def search_films(
        films: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:
        """
        Search films by title, director, or description

        Args:
            films: List of films to search
            query: Search query

        Returns:
            Films matching the query
        """
        query_lower = query.lower()
        results = []

        for film in films:
            title = (film.get('title', '') or '').lower()
            director = (film.get('director', '') or '').lower()
            description = (film.get('description', '') or '').lower()

            if (query_lower in title or
                query_lower in director or
                query_lower in description):
                results.append(film)

        return results

    @staticmethod
    def get_locations(films: List[Dict[str, Any]]) -> List[str]:
        """Get all unique locations from films"""
        locations = set()
        for film in films:
            for screening in film.get('screenings', []):
                location = screening.get('location', '')
                if location:
                    locations.add(location)
        return sorted(list(locations))

    @staticmethod
    def get_directors(films: List[Dict[str, Any]]) -> List[str]:
        """Get all unique directors from films"""
        directors = set()
        for film in films:
            director = film.get('director', '')
            if director:
                directors.add(director)
        return sorted(list(directors))
