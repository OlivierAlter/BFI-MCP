# BFI-MCP Deployment Guide

## Overview

BFI-MCP is optimized for **Alpic cloud deployment** only. No Docker, CodeBuild, or manual containerization needed.

## Quick Deploy

```bash
# 1. Go to https://alpic.ai
# 2. Sign in with GitHub
# 3. Click "New Project"
# 4. Select: OlivierAlter/BFI-MCP
# 5. Click "Create"
# Done! ✅
```

Alpic auto-detects and deploys. You'll get a public HTTPS endpoint in minutes.

## Architecture

```
GitHub (OlivierAlter/BFI-MCP)
         ↓
      Alpic
         ↓
   Auto-detect:
   - pyproject.toml ✓
   - uv.lock ✓
   - mcp_server.py ✓
   - data/ ✓
         ↓
   Build & Deploy
         ↓
   Public HTTPS:
   https://mcp-server-XXXXXXX.alpic.live
```

## How Alpic Works

1. **Detects** Python MCP from `pyproject.toml`
2. **Reads** dependencies from `uv.lock`
3. **Builds** Python environment with `uv sync`
4. **Starts** server with `mcp_server.py`
5. **Exposes** as HTTPS endpoint
6. **Auto-updates** when you push to GitHub

## Using Your MCP

### With Claude Code

Add to `~/.claude/claude_code_config.json`:

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

### With MCP Inspector

```bash
npx @modelcontextprotocol/inspector
# Select: Streamable HTTP
# Enter: https://mcp-server-XXXXXXX.alpic.live
```

## Local Testing

For development without Alpic:

```bash
# Install dependencies
pip install -r requirements.txt

# Start HTTP server
python mcp_server.py

# Server runs on http://127.0.0.1:3000
# Use with MCP Inspector or Claude Code
```

See [SETUP.md](SETUP.md) for detailed local testing.

## What We Removed

To keep BFI-MCP Alpic-focused:

**Removed (CodeBuild):**
- ❌ `buildspec.yml` - AWS CodeBuild config
- ❌ `CODEBUILD_TROUBLESHOOTING.md` - CodeBuild docs

**Removed (Docker):**
- ❌ `Dockerfile` - Manual Docker build
- ❌ `docker-compose.yml` - Local Docker compose
- ❌ `DOCKER.md` - Docker deployment guide
- ❌ `.dockerignore` - Docker build config

**Reason:** Alpic handles all containerization automatically. No manual Docker needed.

## What We Kept

**Core Files:**
- ✅ `mcp_server.py` - HTTP/FastMCP server (auto-started by Alpic)
- ✅ `data_loader.py` - Film data management
- ✅ `filters.py` - Search and filter logic
- ✅ `data/` - All 139 BFI films in JSON

**Configuration:**
- ✅ `pyproject.toml` - Python package metadata (Alpic reads this)
- ✅ `uv.lock` - Locked dependencies (Alpic reads this)
- ✅ `requirements.txt` - Pip requirements (backup)

**Documentation:**
- ✅ `README.md` - Quick overview and setup
- ✅ `ALPIC_SETUP.md` - Primary deployment guide (3 steps!)
- ✅ `SETUP.md` - Local testing guide
- ✅ `INDEX.md` - Tool reference
- ✅ `HTTP_MIGRATION.md` - Migration documentation

## Migration from Old Architecture

**Before:**
- stdio-based MCP
- Custom Dockerfile
- AWS CodeBuild
- Complex setup

**After:**
- HTTP/FastMCP server
- Alpic auto-containerization
- 3-step Alpic deployment
- Zero configuration

## Transport

**Old:** stdio (subprocess for Claude Code)
**New:** Streamable HTTP (cloud service via Alpic)

Benefits:
- ✅ Public HTTPS endpoint
- ✅ Automatic scaling
- ✅ No local server required
- ✅ Easy team sharing
- ✅ Works everywhere (Claude Code, Inspector, APIs)

## Monitoring

Once deployed on Alpic:
- View build logs
- Monitor uptime/health
- See usage analytics
- Manage environment variables
- Trigger rebuilds manually

## Auto-Updates

Push to GitHub → Alpic auto-rebuilds → New version live

No manual deployment steps needed after initial setup.

## Support

- **Alpic Issues**: https://docs.alpic.ai
- **BFI-MCP Issues**: GitHub Issues
- **Local Testing**: See SETUP.md

## Status

✅ **Production Ready**
- HTTP/FastMCP server ✓
- Data files included ✓
- Auto-configuration ✓
- Zero manual steps ✓
- Public endpoint ✓

**Ready to deploy to Alpic!**

---

**See:** [ALPIC_SETUP.md](ALPIC_SETUP.md) for 3-step deployment
**Or:** [SETUP.md](SETUP.md) for local testing

Last Updated: November 8, 2025
