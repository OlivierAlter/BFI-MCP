# Deploy BFI-MCP to Alpic (Primary Guide)

**Alpic** is Anthropic's cloud platform for deploying and scaling Model Context Protocol servers. BFI-MCP is optimized for Alpic with zero configuration needed.

## What is Alpic?

Alpic automatically:
- ✅ Detects Python MCP projects from `pyproject.toml`
- ✅ Builds and containerizes your code
- ✅ Deploys as public HTTPS service
- ✅ Provides scalable HTTP endpoints
- ✅ Handles updates automatically

**Result**: Your MCP is accessible via public HTTPS endpoint in minutes.

## Prerequisites

1. **GitHub Account** - For authentication and code hosting
2. **Alpic Account** - Free at https://alpic.ai
3. **BFI-MCP Repository** - This repo (already configured)

## Deploy in 3 Steps

### Step 1: Go to Alpic
```
https://alpic.ai
```

### Step 2: Sign In with GitHub
Click "Sign in with GitHub" and authorize access to your repositories.

### Step 3: Create Project
1. Click "New Project"
2. Select: `OlivierAlter/BFI-MCP`
3. Primary Branch: `main`
4. Click "Create"

**That's it!** Alpic will:
- ✅ Detect `pyproject.toml` (package config)
- ✅ Read `uv.lock` (locked dependencies)
- ✅ Build Python environment
- ✅ Start `python mcp_server.py`
- ✅ Deploy as HTTPS service
- ✅ Provide public endpoint

## No Configuration Needed

BFI-MCP is pre-configured for Alpic:
- ✅ `pyproject.toml` - Package metadata
- ✅ `uv.lock` - Dependency lock file
- ✅ `mcp_server.py` - Entry point
- ✅ `data/` - All film data included
- ✅ `.gitignore` - Excludes unnecessary files

Alpic auto-detects all of this. Zero manual configuration required.

## After Deployment

Alpic will show your deployment with a public HTTPS endpoint:

```
https://mcp-server-XXXXXXX.alpic.live
```

### Use with Claude Code

Add to your Claude Code config (`~/.claude/claude_code_config.json`):

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

Restart Claude Code and use `@bfi` commands.

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

1. Select **Streamable HTTP**
2. Enter: `https://mcp-server-XXXXXXX.alpic.live`
3. Click "Connect"
4. Test: list-films, search-films, get-film-details

## Auto-Updates

When you push changes to GitHub:
1. Alpic detects the update automatically
2. Rebuilds and redeploys
3. New version live within minutes
4. No manual intervention needed

## Status Dashboard

In Alpic:
- View deployment logs
- Monitor uptime
- See usage analytics
- Manage environments

## Troubleshooting

### Deployment Failed

Check Alpic dashboard logs. Most common issues:
- Missing `pyproject.toml` ✓ (we have it)
- Missing `uv.lock` ✓ (we have it)
- Missing data files ✓ (all included)

### MCP Inspector Won't Connect

1. Check endpoint URL is correct (copy from Alpic)
2. Check deployment status is "Active"
3. Try endpoint in browser to verify accessibility

### Issues

- **Alpic Docs**: https://docs.alpic.ai
- **BFI-MCP Issues**: See README.md or GitHub issues

---

**Status**: ✅ Ready for Alpic deployment
**Setup Time**: ~5 minutes
**Transport**: HTTP via FastMCP
**Deployment**: Cloud (Alpic) + local testing available
**Last Updated**: November 8, 2025
