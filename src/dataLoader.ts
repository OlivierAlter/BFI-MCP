import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export interface Screening {
  date: string;
  time: string;
  location: string;
}

export interface Film {
  title: string;
  description?: string;
  country_year?: string;
  director?: string;
  cast?: string;
  runtime?: string;
  format?: string;
  rating?: string;
  screenings: Screening[];
  category?: string;
}

let filmsCache: Film[] | null = null;

export const loadFilms = (): Film[] => {
  if (filmsCache) {
    return filmsCache;
  }

  const dataDir = join(__dirname, "..", "data");
  const allFilmsPath = join(dataDir, "bfi_all_films.json");

  try {
    const data = readFileSync(allFilmsPath, "utf-8");
    const parsed = JSON.parse(data);
    // Extract films array from the nested JSON structure
    filmsCache = (parsed.films || parsed) as Film[];
    console.log(`✓ Loaded ${filmsCache.length} films`);
    return filmsCache;
  } catch (error) {
    console.error("Error loading film data:", error);
    throw new Error("Failed to load film data");
  }
};

export const getFilmByTitle = (title: string): Film | undefined => {
  const films = loadFilms();
  return films.find((film) => film.title.toLowerCase() === title.toLowerCase());
};

export const searchFilms = (query: string, limit = 20): Film[] => {
  const films = loadFilms();
  const lowerQuery = query.toLowerCase();

  return films
    .filter(
      (film) =>
        film.title.toLowerCase().includes(lowerQuery) ||
        film.director?.toLowerCase().includes(lowerQuery) ||
        film.description?.toLowerCase().includes(lowerQuery),
    )
    .slice(0, limit);
};

export const filterFilms = (params: {
  category?: string;
  location?: string;
  director?: string;
  startDate?: string;
  endDate?: string;
  limit?: number;
}): Film[] => {
  const { category, location, director, startDate, endDate, limit = 50 } = params;
  let films = loadFilms();

  if (category) {
    films = films.filter((film) => film.category === category);
  }

  if (director) {
    const lowerDirector = director.toLowerCase();
    films = films.filter((film) => film.director?.toLowerCase().includes(lowerDirector));
  }

  if (location || startDate || endDate) {
    films = films
      .map((film) => {
        const filteredScreenings = film.screenings.filter((screening) => {
          if (location && !screening.location.toLowerCase().includes(location.toLowerCase())) {
            return false;
          }
          if (startDate && screening.date < startDate) {
            return false;
          }
          if (endDate && screening.date > endDate) {
            return false;
          }
          return true;
        });

        return filteredScreenings.length > 0 ? { ...film, screenings: filteredScreenings } : null;
      })
      .filter((film): film is Film => film !== null);
  }

  return films.slice(0, limit);
};
