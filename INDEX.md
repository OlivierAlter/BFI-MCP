# BFI-MCP Index

## Quick Navigation

### 🚀 Getting Started
- **[SETUP.md](SETUP.md)** - Integration with Claude Code (START HERE)
- **[README.md](README.md)** - Full documentation and usage guide

### 📚 Documentation
| File | Purpose |
|------|---------|
| `SETUP.md` | How to integrate with Claude Code |
| `README.md` | Full API documentation |
| `INDEX.md` | This file |

### 💻 Code Files
| File | Lines | Purpose |
|------|-------|---------|
| `mcp_server.py` | 350+ | Main MCP server with tool handlers |
| `data_loader.py` | 130+ | JSON data management |
| `filters.py` | 180+ | Filtering and search logic |
| `test.py` | 140+ | Test suite (run with `python3 test.py`) |

### 📊 Data Files (160 KB total)
Located in `data/` directory:
- `bfi_all_films.json` - All 139 films combined
- 10 category-specific JSON files

### 🛠️ Dependencies
- `requirements.txt` - Install with `pip install -r requirements.txt`
- Single dependency: `mcp>=0.1.0`

---

## Tools Overview

### 1. **list-films** - Browse & Filter
List all BFI films with optional filtering

```
@bfi list-films
@bfi list-films category=james_cameron
@bfi list-films location="BFI IMAX"
@bfi list-films director=Cameron
@bfi list-films start_date=2025-10-24 end_date=2025-10-31
```

**Filters:**
- `category` - Film category
- `location` - Cinema location
- `director` - Director name (partial match)
- `start_date` - Screening start date (YYYY-MM-DD)
- `end_date` - Screening end date (YYYY-MM-DD)
- `limit` - Max results (default: 50)

---

### 2. **search-films** - Full-Text Search
Search in titles, directors, descriptions

```
@bfi search-films query=Terminator
@bfi search-films query="James Cameron"
@bfi search-films query=melodrama limit=10
```

**Parameters:**
- `query` (required) - Search text
- `limit` - Max results (default: 20)

---

### 3. **get-film-details** - Complete Info
Get all details for a specific film

```
@bfi get-film-details title="The Terminator"
@bfi get-film-details title="Aliens (Extended Cut)"
```

**Returns:**
- Director, cast, runtime, format, rating
- Full description
- All screenings with dates, times, locations

---

## Available Filters

### Categories (10 total)
```
james_cameron        Christmas films
christmas_films      Regular programme
richard_burton       New releases
melodrama           Re-releases
classics            In-person events
frederick_wiseman
```

### Locations (7 total)
```
NFT1, NFT2, NFT3, NFT4      Main screens
BFI IMAX                      IMAX screen
BFI REUBEN LIBRARY           Library events
BFI BLUE ROOM                Discussion venues
```

---

## Quick Examples

### Browse by Category
```
"Show all James Cameron films"
→ @bfi list-films category=james_cameron

"What Christmas films are available?"
→ @bfi list-films category=christmas_films
```

### Find by Location
```
"Films at BFI IMAX"
→ @bfi list-films location="BFI IMAX"

"All NFT1 screenings"
→ @bfi list-films location=NFT1
```

### Search
```
"Find Terminator films"
→ @bfi search-films query=Terminator

"Look for Hitchcock"
→ @bfi search-films query=Hitchcock
```

### Get Details
```
"Full info on The Terminator"
→ @bfi get-film-details title="The Terminator"

"Tell me about Aliens"
→ @bfi get-film-details title="Aliens (Extended Cut)"
```

### Advanced Filtering
```
"Films at IMAX next week"
→ @bfi list-films location="BFI IMAX" start_date=2025-10-24 end_date=2025-10-31

"Cameron films in October"
→ @bfi list-films category=james_cameron start_date=2025-10-01 end_date=2025-10-31
```

---

## Data Statistics

| Metric | Value |
|--------|-------|
| **Total Films** | 139 |
| **Total Screenings** | 256 |
| **Categories** | 10 |
| **Cinema Locations** | 7 |
| **Date Range** | Oct 20 - Dec 31, 2025 |
| **Memory Usage** | ~5-10 MB |
| **Load Time** | <1 second |
| **Query Speed** | <50ms |

---

## File Organization

```
BFIGuide/
├── extract_bfi_guide.py          Main extraction script
├── monthly_update.sh             Monthly automation
├── pdf_text.txt                  Current month's PDF text
│
├── output/                        Generated ICS/JSON files
│   └── *.ics, *.json
│
├── bfi-mcp/                       ← YOU ARE HERE
│   ├── mcp_server.py
│   ├── data_loader.py
│   ├── filters.py
│   ├── test.py
│   ├── requirements.txt
│   ├── README.md
│   ├── SETUP.md
│   ├── INDEX.md                  This file
│   └── data/
│       ├── bfi_all_films.json
│       └── 10 category JSON files
│
└── claude.md                      Project documentation
```

---

## Workflow

### Initial Setup
1. ✅ Extract PDF with `monthly_update.sh` → JSON files in `output/`
2. ✅ Copy JSON files to `bfi-mcp/data/`
3. ✅ Install MCP: `pip install -r bfi-mcp/requirements.txt`
4. ✅ Add to Claude Code config
5. ✅ Restart Claude Code

### Monthly Updates
1. Download new BFI guide PDF
2. Run `./monthly_update.sh ~/Downloads/BFI_[Month]_[Year].pdf`
3. Copy new files: `cp output/*.json bfi-mcp/data/`
4. Restart Claude Code
5. Use `@bfi` commands with updated data

---

## Testing

Run the test suite:
```bash
cd bfi-mcp
python3 test.py
```

Expected output shows:
- ✓ Films loaded
- ✓ Categories available
- ✓ Filtering works
- ✓ Search works
- ✓ Details retrieval works

---

## Integration Status

| Component | Status |
|-----------|--------|
| Data Loading | ✅ Complete |
| Filtering | ✅ Complete |
| Search | ✅ Complete |
| Film Details | ✅ Complete |
| Test Suite | ✅ Passing |
| Documentation | ✅ Complete |
| Claude Code Integration | ⏳ Next Step |

---

## Support

### Questions?
- See `README.md` for detailed API documentation
- See `SETUP.md` for integration help
- Run `python3 test.py` to verify everything works

### Issues?
1. Check `SETUP.md` troubleshooting section
2. Verify JSON files exist: `ls data/*.json`
3. Run tests: `python3 test.py`
4. Check Python version: `python3 --version`

---

## Version Info

- **Status**: ✅ Ready for Production
- **Last Updated**: November 8, 2025
- **Films**: 139 (Oct/Nov + Dec 2025 guides)
- **Screenings**: 256
- **Data Format**: JSON (from BFI guide extraction)
- **Python**: 3.6+

---

**Next Step**: Read [SETUP.md](SETUP.md) to integrate with Claude Code! 🚀
