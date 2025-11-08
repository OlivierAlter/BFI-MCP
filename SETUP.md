# Local Testing & Development

**For Production Deployment**: See [ALPIC_SETUP.md](ALPIC_SETUP.md) to deploy to Alpic cloud.

This guide covers local testing of the HTTP server for development and debugging.

## Quick Start (HTTP Server)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the MCP SDK with HTTP/Streamable HTTP support.

### 2. Run the HTTP Server Locally

Start the MCP server on port 3000:

```bash
python mcp_server.py
```

Output:
```
✓ Loaded 139 films, 256 screenings
Uvicorn running on http://127.0.0.1:3000
```

### 3. Test with MCP Inspector

In another terminal:

```bash
npx @modelcontextprotocol/inspector
```

1. Select **Streamable HTTP** transport
2. Enter: `http://127.0.0.1:3000/mcp`
3. Click "Connect"
4. Test the tools in the inspector

### 4. Use with Claude Code (via HTTP)

Configure Claude Code to connect to the HTTP server:

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

**Note**: Keep the HTTP server running while using Claude Code (run `python mcp_server.py` in a terminal).

### 5. Deploy to Alpic (Recommended)

See [ALPIC_SETUP.md](ALPIC_SETUP.md) for production deployment instructions.

---

## Test Without Integration

To test the MCP without Claude Code integration:

```bash
cd /path/to/bfi-mcp
python3 test.py
```

Expected output:
```
============================================================
  BFI-MCP Test Suite
============================================================

Test 1: Loading data...
✓ Loaded 139 films
✓ Total screenings: 256
```

---

## Available Tools

### list-films
List and filter BFI films

```
@bfi list-films
@bfi list-films category=christmas_films
@bfi list-films location="BFI IMAX"
@bfi list-films director=Cameron
@bfi list-films start_date=2025-10-24 end_date=2025-10-31
```

### search-films
Full-text search in titles, directors, descriptions

```
@bfi search-films query=Terminator
@bfi search-films query="James Cameron"
@bfi search-films query=melodrama
```

### get-film-details
Get complete information about a specific film

```
@bfi get-film-details title="The Terminator"
@bfi get-film-details title="Aliens (Extended Cut)"
```

---

## Updating Film Data

When new BFI guides are available:

### 1. Generate new JSON files
```bash
cd /path/to/BFIGuide
./monthly_update.sh ~/Downloads/BFI_[Month]_[Year].pdf
```

### 2. Copy to MCP data directory
```bash
cp output/*.json bfi-mcp/data/
```

### 3. Restart Claude Code
The MCP will auto-reload the new data at startup.

---

## Troubleshooting

### MCP not showing up
- Check the config file path is correct
- Verify the Python path is absolute (starts with `/`)
- Make sure `mcp` package is installed: `pip list | grep mcp`
- Check Claude Code logs for errors

### Films not loading
- Verify JSON files exist: `ls bfi-mcp/data/*.json`
- Test directly: `python3 test.py`
- Check file permissions: `chmod 644 bfi-mcp/data/*.json`

### Search returns no results
- Search is case-insensitive but requires exact words
- Try shorter search terms
- Use `list-films` with filters instead

---

## File Structure

```
bfi-mcp/
├── mcp_server.py          MCP server implementation
├── data_loader.py         JSON data loader
├── filters.py             Filtering and search logic
├── test.py                Test suite
├── requirements.txt       Python dependencies
├── README.md              Full documentation
├── SETUP.md              This file
└── data/                  JSON data files
    ├── bfi_all_films.json
    ├── bfi_james_cameron.json
    ├── bfi_classics.json
    └── ... (9 other category files)
```

---

## How It Works

1. **At startup**: MCP server loads all JSON files from `data/` directory
2. **In-memory**: All 139 films stored in memory (~5-10 MB)
3. **On request**: Filters/searches run against in-memory data (<50ms)
4. **Response**: Formatted text response returned to Claude Code

---

## Features

✅ Load 139+ films at startup
✅ Search full-text in title/director/description
✅ Filter by category, location, director, date
✅ Get complete film details and screenings
✅ Zero latency queries (<50ms)
✅ Auto-update when data files change

---

## Next Steps

1. ✅ Test with `python3 test.py`
2. ✅ Add to Claude Code config
3. ✅ Restart Claude Code
4. ✅ Try: `@bfi list-films category=james_cameron`
5. ✅ Enjoy discovering BFI films!

---

**Questions?** See README.md for more details.

**Status**: ✅ Ready to use
**Last Updated**: November 8, 2025
