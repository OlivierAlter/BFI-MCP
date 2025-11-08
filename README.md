# BFI-MCP: Claude MCP for BFI Southbank Films

A high-performance Model Context Protocol (MCP) server for accessing BFI Southbank film screenings data with intelligent filtering and search. Built with **TypeScript/Node.js** using the official MCP SDK and optimized for **Alpic** cloud deployment.

## Features

✅ **139 BFI Films** - Complete metadata, descriptions, and screenings
✅ **Smart Filtering** - Filter by category, location, director, date range
✅ **Full-Text Search** - Search in titles, directors, descriptions
✅ **Complete Details** - Screenings, ratings, cast, runtime, format
✅ **Express.js HTTP Server** - Streamable HTTP MCP transport
✅ **TypeScript/Node.js** - Type-safe, modern JavaScript backend
✅ **Alpic Ready** - Automatic deployment with zero configuration

## Quick Start: Deploy to Alpic

See **[ALPIC_SETUP.md](ALPIC_SETUP.md)** for complete deployment instructions.

### 1-Minute Setup

1. Go to https://alpic.ai
2. Sign in with GitHub
3. Click "New Project"
4. Select `OlivierAlter/BFI-MCP`
5. Click "Create"
6. Alpic auto-detects and deploys
7. Get your public endpoint

That's it! Your MCP is live.

## Local Testing

### Install Dependencies

```bash
npm install
```

### Build TypeScript

```bash
npm run build
```

### Run HTTP Server Locally

```bash
npm start
```

Server runs on `http://127.0.0.1:3000/mcp` (POST endpoint)

### Test with MCP Inspector

```bash
npm run inspector
```

Or use npx directly:
```bash
npx @modelcontextprotocol/inspector
```

Select **Streamable HTTP** → Enter `http://127.0.0.1:3000/mcp`

### Development Mode

For hot-reload during development:

```bash
npm run dev
```

Watches TypeScript files and restarts on changes.

### Configure for Claude Code

To use with Claude Code locally:

```json
{
  "mcpServers": {
    "bfi": {
      "url": "http://127.0.0.1:3000/mcp",
      "transport": "http"
    }
  }
}
```

**Note:** Keep `npm start` running while using Claude Code.

## Using Your Deployed MCP

Once deployed on Alpic, integrate with Claude Code:

```json
{
  "mcpServers": {
    "bfi": {
      "url": "https://mcp-server-XXXXXXX.alpic.live",
      "transport": "http"
    }
  }
}
```

Or use with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Select **Streamable HTTP** → Enter your Alpic endpoint

---

## Scripts

### Available npm commands:

```bash
npm run build        # Compile TypeScript to JavaScript
npm start           # Start production server on port 3000
npm run dev         # Start development server with hot-reload
npm run inspector   # Launch MCP Inspector for testing
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

### Project Structure

```
src/
├── index.ts          Express HTTP server with /mcp endpoint
├── server.ts         MCP server with 3 tools (Zod schemas)
├── dataLoader.ts     Film data loading and filtering
├── config.ts         Configuration (PORT, paths)
└── data/             JSON data files
    └── bfi_*.json    Film data by category

dist/                 Compiled JavaScript (generated by tsc)
├── index.js
├── server.js
├── dataLoader.js
└── config.js
```

### Tech Stack

- **Runtime**: Node.js 20+
- **Language**: TypeScript 5.x
- **Framework**: Express.js 5.x
- **MCP SDK**: @modelcontextprotocol/sdk
- **Schema Validation**: Zod
- **Build**: TypeScript compiler (tsc)

### Key Files

- **src/index.ts**: Express app setup, /mcp endpoint handler
- **src/server.ts**: MCP server configuration and tool definitions
- **src/dataLoader.ts**: Film data loading, filtering, and search
- **package.json**: Dependencies and npm scripts
- **tsconfig.json**: TypeScript compiler configuration

---

## Development

### Understanding the Code

The MCP server implements 3 tools using the official SDK:

```typescript
// Tools are defined with Zod schemas for type safety
server.tool("list-films", description, schema, handler)
server.tool("search-films", description, schema, handler)
server.tool("get-film-details", description, schema, handler)
```

Each tool handler:
1. Receives validated parameters (Zod ensures type safety)
2. Calls dataLoader functions
3. Returns formatted CallToolResult with content

### Testing Tools Locally

Build and start the server:
```bash
npm run build
npm start
```

Use MCP Inspector to test:
```bash
npm run inspector
```

Or test directly:
```bash
curl -X POST http://127.0.0.1:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{...},"id":1}'
```

---

## License

Personal use. BFI Guide data from BFI Southbank, used with permission for calendar parsing.

---

## Summary

| Aspect | Details |
|--------|---------|
| **Status** | ✅ Production Ready |
| **Language** | TypeScript/Node.js |
| **Framework** | Express.js + MCP SDK |
| **Films** | 139 (Combined BFI database) |
| **Screenings** | 256 (Oct/Nov 2025) |
| **Deployment** | Alpic (recommended) or Docker/Manual |
| **Last Updated** | November 8, 2025 |
| **Port** | 3000 (local) |
| **Endpoint** | `http://localhost:3000/mcp` |

Get started:
```bash
npm install && npm run build && npm start
```

Then test with:
```bash
npm run inspector
```
