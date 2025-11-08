# BFI-MCP: Claude MCP for BFI Southbank Films

A Model Context Protocol (MCP) server that provides access to BFI Southbank film screenings data with intelligent filtering and search.

## Features

✅ **Access all BFI films** - 139 films with complete metadata
✅ **Smart filtering** - Filter by category, location, director, date range
✅ **Full-text search** - Search in titles, directors, descriptions
✅ **Complete details** - Get screenings, metadata, ratings, descriptions
✅ **Two deployment options** - Claude Code (local) or Alpic (cloud HTTP)
✅ **Zero hidden dependencies** - Uses existing JSON data files

## Installation

Choose one of two deployment options:

### Option A: Claude Code (Local) - Recommended for Personal Use

See **[SETUP.md](SETUP.md)** for complete instructions on integrating with Claude Code as a local subprocess.

### Option B: Alpic (Cloud) - Recommended for Team Use

See **[ALPIC_SETUP.md](ALPIC_SETUP.md)** for deploying to Alpic as a public HTTP service.

---

## Quick Start: Claude Code

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Update Claude Code Config

Add this to your Claude Code MCP configuration (usually in `~/.claude/claude_code_config.json` or your MCP config):

```json
{
  "mcps": {
    "bfi": {
      "command": "python",
      "args": ["/path/to/bfi-mcp/mcp_server.py"]
    }
  }
}
```

Replace `/path/to/bfi-mcp/` with the actual path to the bfi-mcp directory.

### 3. Restart Claude Code

```bash
# Your editor will need to restart to load the new MCP
```

## Tools

### 1. `list-films` - List and filter films

List all BFI films with optional filtering.

**Parameters:**
- `category` (optional) - Filter by category
- `location` (optional) - Filter by cinema location
- `director` (optional) - Filter by director name
- `start_date` (optional) - Filter screenings from date (YYYY-MM-DD)
- `end_date` (optional) - Filter screenings until date (YYYY-MM-DD)
- `limit` (optional) - Max results to return (default: 50)

**Examples:**

```
"Show me all Christmas films"
→ Uses: category="christmas_films"

"List films at BFI IMAX"
→ Uses: location="BFI IMAX"

"Show all James Cameron films"
→ Uses: category="james_cameron"

"Find screenings between October 20 and November 5"
→ Uses: start_date="2025-10-20", end_date="2025-11-05"

"Show melodrama films by Sirk"
→ Uses: category="melodrama", director="Sirk"
```

---

### 2. `search-films` - Full-text search

Search for films by title, director, or description.

**Parameters:**
- `query` (required) - Search query
- `limit` (optional) - Max results (default: 20)

**Examples:**

```
"Find 'Terminator' films"
"Search for Hitchcock"
"Find films about love"
"Look for 'sci-fi'"
```

---

### 3. `get-film-details` - Get complete film information

Retrieve full details for a specific film including all screenings.

**Parameters:**
- `title` (required) - Exact film title

**Returns:**
- Film metadata (director, cast, runtime, format, rating)
- Full description
- All screenings with dates, times, locations

**Examples:**

```
"Get details on The Terminator"
"Show me all info about Aliens"
"What time is Brief Encounter screening?"
```

---

## Available Filters

### Categories
- `james_cameron` - James Cameron retrospective
- `christmas_films` - Holiday programming
- `richard_burton` - Richard Burton retrospective
- `melodrama` - "Too Much: Melodrama on Film" series
- `classics` - Big Screen Classics
- `frederick_wiseman` - Frederick Wiseman documentaries
- `in_person` - Events and Q&As
- `new_releases` - New theatrical releases
- `re_releases` - Classic re-releases
- `regular_programme` - Special screenings

### Locations
- `NFT1`, `NFT2`, `NFT3`, `NFT4` - Main cinema screens
- `BFI IMAX` - IMAX screen
- `BFI REUBEN LIBRARY` - Library events
- `BFI BLUE ROOM` - Discussion venues
- `BFI BAR` - Bar/lounge area
- `BFI SOUTHBANK FOYER` - Foyer events

---

## Use Cases

### Planning Your Cinema Visit
```
"I want to watch films at BFI IMAX this month. What's available?"
→ list-films(location="BFI IMAX", start_date="2025-11-08", end_date="2025-11-30")
```

### Finding Specific Directors
```
"Show me all Laura Mulvey films screening"
→ search-films(query="Laura Mulvey")
```

### Category Browsing
```
"What are the classic films screening?"
→ list-films(category="classics")
```

### Full Film Details
```
"I want to know everything about Aliens"
→ get-film-details(title="Aliens (Extended Cut)")
```

---

## Data Structure

The MCP loads data from JSON files in the `data/` directory:

```
data/
├── bfi_all_films.json           (Combined all films)
├── bfi_james_cameron.json       (Category-specific)
├── bfi_classics.json
├── bfi_christmas_films.json
├── bfi_melodrama.json
├── bfi_richard_burton.json
├── bfi_frederick_wiseman.json
├── bfi_new_releases.json
├── bfi_re_releases.json
└── bfi_regular_programme.json
```

**Load Time**: Startup only (under 1 second)
**Data Freshness**: Manual - copy new JSON files from `../output/` when available

---

## Updating Film Data

When new BFI guides are released:

1. Generate new JSON files:
   ```bash
   cd ..
   ./monthly_update.sh ~/Downloads/BFI_[Month]_[Year].pdf
   ```

2. Copy updated files to MCP:
   ```bash
   cp ../output/*.json data/
   ```

3. Restart Claude Code to reload data

---

## Error Handling

- **Film not found**: Returns error message
- **Invalid date format**: Ignores invalid dates
- **Empty search**: Returns error
- **Data load failure**: Server reports error at startup

---

## Performance

- **Load time**: <1 second (at startup)
- **List films**: <10ms
- **Search**: <50ms
- **Get details**: <1ms
- **Memory**: ~5-10 MB

---

## Architecture

```
mcp_server.py          Main MCP server implementing tool handlers
├── data_loader.py     Loads JSON files and manages data
├── filters.py         Filtering and searching logic
└── data/              JSON data files
    └── bfi_*.json     Film data by category
```

---

## Development

### Testing Tools Locally

```python
from data_loader import BFIDataLoader
from filters import FilmFilter

# Load data
loader = BFIDataLoader("./data")
films = loader.get_all_films()

# Test filtering
cameron_films = FilmFilter.filter_films(
    films,
    category="james_cameron"
)

# Test search
results = FilmFilter.search_films(films, "Terminator")

# Get film details
film = loader.get_film_by_title("The Terminator")
```

---

## License

Personal use. BFI Guide data from BFI Southbank, used with permission for calendar parsing.

---

**Status**: ✅ Ready for use
**Last Updated**: November 8, 2025
**Films**: 93 (Oct/Nov 2025 guide)
**Screenings**: 158
