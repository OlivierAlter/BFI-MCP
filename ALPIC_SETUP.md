# Alpic Deployment Guide for BFI-MCP

This guide explains how to deploy BFI-MCP on Alpic, Anthropic's MCP hosting platform.

## Overview

**Alpic** is a platform for hosting and distributing MCP servers. Unlike Claude Code (which runs MCPs locally as subprocesses), Alpic runs MCPs as **HTTP web services** that can be accessed remotely.

**Key Difference:**
- **Claude Code**: Runs MCP as stdio subprocess locally
- **Alpic**: Runs MCP as HTTP server in the cloud

## Prerequisites

1. **Alpic Account**: https://alpic.ai
2. **GitHub Account**: For source code hosting
3. **GitHub App**: Alpic AI app installed on your organization

## Initial Setup (One-time)

### Step 1: Connect GitHub to Alpic

1. Go to https://alpic.ai
2. Click "Sign in with GitHub"
3. Authorize Alpic to access your repositories
4. Create a Team in Alpic

### Step 2: Create a Project

1. In Alpic dashboard, click "New Project"
2. Select the BFI-MCP repository
3. Set **Primary Branch** to: `main`
4. Click "Create Project"

## Configuration in Alpic

### Build Configuration

Alpic should **auto-detect** the build configuration from `pyproject.toml` and `uv.lock`.

If manual configuration is needed:

**Install Command:**
```
uv sync
```

**Build Command (Optional):**
```
python test.py
```

**Build Output Directory:**
```
/app
```

**Start Command:**
```
python mcp_server.py
```

### Environment Variables

Add any required environment variables in Alpic's project settings:
- Currently: None required
- Format: `KEY=value` pairs

## After Deployment

Once deployed, Alpic provides:

### Public Endpoint
```
https://mcp-server-XXXXXXX.alpic.live
```

### Integration with Claude Code

To use Alpic-hosted BFI-MCP with Claude Code:

Add to your Claude Code config:
```json
{
  "mcpServers": {
    "bfi-alpic": {
      "url": "https://mcp-server-XXXXXXX.alpic.live",
      "transport": "http"
    }
  }
}
```

### Testing with MCP Inspector

After deployment, test with:
```bash
npx @modelcontextprotocol/inspector
```

1. Select **Streamable HTTP** transport
2. Enter: `https://mcp-server-XXXXXXX.alpic.live`
3. Click "Connect"
4. Test tools: list-films, search-films, get-film-details

## Updating Data

When you have new BFI film data:

1. Update JSON files in `data/` directory
2. Commit and push to `main` branch
3. Alpic automatically rebuilds and deploys
4. New data is available via the HTTP endpoint

## Troubleshooting

### Build Fails

**Check:**
- ✓ `pyproject.toml` exists (defines package)
- ✓ `uv.lock` exists (locks dependencies)
- ✓ `mcp_server.py` exists and is executable
- ✓ Data files in `data/` directory are included

**Rebuild:**
- In Alpic dashboard, click "Rebuild" on your project
- Check build logs in the UI

### Connection Issues

**MCP Inspector won't connect:**
1. Verify endpoint URL is correct
2. Check if deployment is "Active" in Alpic
3. Try accessing URL in browser (should show connection info)

### HTTP vs Stdio

**Our Implementation:**
- Primary transport: **stdio** (for Claude Code local use)
- Alpic transport: **HTTP** (Alpic wraps the stdio server)

This means:
- ✅ Works with Claude Code locally (stdio)
- ✅ Works with Alpic remotely (HTTP)
- ✅ Works with MCP Inspector (HTTP)

## Deployment Status

Once deployed:
- [ ] Alpic shows "Active" status
- [ ] Public endpoint accessible
- [ ] MCP Inspector can connect
- [ ] Tools respond to queries

## Support

For Alpic-specific issues: https://docs.alpic.ai

For BFI-MCP issues: See README.md

---

**Status**: Ready for Alpic deployment
**Configuration**: Auto-detected from pyproject.toml + uv.lock
**Transport**: HTTP (Alpic manages)
**Last Updated**: November 8, 2025
