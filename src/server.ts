import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { type CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { getFilmByTitle, searchFilms, filterFilms, loadFilms, type Film } from "./dataLoader.js";

const formatFilm = (film: Film, includeScreenings = true): string => {
  const lines: string[] = [];

  lines.push(`🎬 ${film.title}`);
  if (film.country_year) lines.push(`Country/Year: ${film.country_year}`);
  if (film.director) lines.push(`Director: ${film.director}`);
  if (film.cast) {
    const cast = film.cast.length > 100 ? film.cast.substring(0, 100) + "..." : film.cast;
    lines.push(`Cast: ${cast}`);
  }
  if (film.runtime) lines.push(`Runtime: ${film.runtime}`);
  if (film.format) lines.push(`Format: ${film.format}`);
  if (film.rating) lines.push(`Rating: ${film.rating}`);

  if (film.description) {
    lines.push("");
    lines.push(`Description:\n${film.description}`);
  }

  if (includeScreenings && film.screenings && film.screenings.length > 0) {
    lines.push("");
    lines.push(`Screenings (${film.screenings.length} total):`);
    film.screenings.forEach((screening) => {
      lines.push(`  • ${screening.date} at ${screening.time} (${screening.location})`);
    });
  }

  return lines.join("\n");
};

export const getServer = (): McpServer => {
  const server = new McpServer(
    {
      name: "bfi-mcp",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    },
  );

  // Load films on server startup
  loadFilms();

  // Tool 1: List films with optional filters
  server.tool(
    "list-films",
    "List all BFI films with optional filtering by category, location, director, or date range",
    {
      category: z
        .string()
        .optional()
        .describe("Filter by category (e.g., 'james_cameron', 'christmas_films', 'classics')"),
      location: z.string().optional().describe("Filter by cinema location (e.g., 'NFT1', 'BFI IMAX')"),
      director: z.string().optional().describe("Filter by director name (partial match)"),
      start_date: z.string().optional().describe("Filter screenings from date (YYYY-MM-DD)"),
      end_date: z.string().optional().describe("Filter screenings until date (YYYY-MM-DD)"),
      limit: z.number().int().positive().default(50).describe("Maximum number of films to return"),
    },
    async ({ category, location, director, start_date, end_date, limit }): Promise<CallToolResult> => {
      const films = filterFilms({
        category,
        location,
        director,
        startDate: start_date,
        endDate: end_date,
        limit,
      });

      if (films.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: "No films found matching the criteria.",
            },
          ],
        };
      }

      const lines = [`Found ${films.length} film(s):\n`];
      films.forEach((film) => {
        const screeningCount = film.screenings.length;
        lines.push(
          `• ${film.title}\n  Director: ${film.director || "Unknown"} | Runtime: ${film.runtime || "Unknown"} | Rating: ${film.rating || "Not rated"}\n  Screenings: ${screeningCount}\n`,
        );
      });

      return {
        content: [
          {
            type: "text",
            text: lines.join("\n"),
          },
        ],
      };
    },
  );

  // Tool 2: Search films by keyword
  server.tool(
    "search-films",
    "Search for films by title, director, or description",
    {
      query: z.string().describe("Search query"),
      limit: z.number().int().positive().default(20).describe("Maximum number of results to return"),
    },
    async ({ query, limit }): Promise<CallToolResult> => {
      if (!query.trim()) {
        return {
          content: [
            {
              type: "text",
              text: "Error: Search query cannot be empty",
            },
          ],
        };
      }

      const results = searchFilms(query, limit);

      if (results.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `No films found matching '${query}'.`,
            },
          ],
        };
      }

      const lines = [`Found ${results.length} film(s) matching '${query}':\n`];
      results.forEach((film) => {
        const screeningCount = film.screenings.length;
        lines.push(`• ${film.title}\n  Director: ${film.director || "Unknown"}\n  Screenings: ${screeningCount}\n`);
      });

      return {
        content: [
          {
            type: "text",
            text: lines.join("\n"),
          },
        ],
      };
    },
  );

  // Tool 3: Get film details
  server.tool(
    "get-film-details",
    "Get complete details for a specific film including screenings and metadata",
    {
      title: z.string().describe("Film title (exact match)"),
    },
    async ({ title }): Promise<CallToolResult> => {
      if (!title.trim()) {
        return {
          content: [
            {
              type: "text",
              text: "Error: Title cannot be empty",
            },
          ],
        };
      }

      const film = getFilmByTitle(title);

      if (!film) {
        return {
          content: [
            {
              type: "text",
              text: `Film '${title}' not found`,
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: formatFilm(film),
          },
        ],
      };
    },
  );

  return server;
};
