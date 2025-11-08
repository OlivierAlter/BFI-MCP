"""
BFI-MCP Data Loader
Loads all JSON film data at startup
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class BFIDataLoader:
    """Loads and manages BFI film data from JSON files"""

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.films: List[Dict[str, Any]] = []
        self.categories = {}
        self._load_all_films()

    def _load_all_films(self):
        """Load all JSON files from data directory"""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        json_files = sorted(self.data_dir.glob("bfi_*.json"))

        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {self.data_dir}")

        # Load all films from all JSON files
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    if 'films' in data:
                        for film in data['films']:
                            self.films.append(film)

                            # Track categories
                            category = film.get('category', 'unknown')
                            if category not in self.categories:
                                self.categories[category] = []
                            self.categories[category].append(film)

            except json.JSONDecodeError as e:
                print(f"Error loading {json_file}: {e}")

        # Remove duplicates (same film might be in multiple category files)
        self._remove_duplicates()

    def _remove_duplicates(self):
        """Remove duplicate films by title"""
        seen_titles = set()
        unique_films = []

        for film in self.films:
            title = film.get('title', '')
            if title not in seen_titles:
                seen_titles.add(title)
                unique_films.append(film)

        self.films = unique_films

        # Rebuild categories
        self.categories = {}
        for film in self.films:
            category = film.get('category', 'unknown')
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(film)

    def get_all_films(self) -> List[Dict[str, Any]]:
        """Get all films"""
        return self.films

    def get_film_by_title(self, title: str) -> Dict[str, Any] | None:
        """Get a single film by exact title match"""
        for film in self.films:
            if film.get('title', '').lower() == title.lower():
                return film
        return None

    def get_films_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all films in a category"""
        return self.categories.get(category.lower(), [])

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return sorted(list(self.categories.keys()))

    def get_film_count(self) -> int:
        """Get total number of unique films"""
        return len(self.films)

    def get_total_screenings(self) -> int:
        """Get total number of screenings across all films"""
        return sum(len(film.get('screenings', [])) for film in self.films)
