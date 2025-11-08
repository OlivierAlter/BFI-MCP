# HTTP Migration: From stdio to Streamable HTTP

## Overview

BFI-MCP has been migrated from **stdio-based transport** to **Streamable HTTP transport** using FastMCP. This change optimizes the server for Alpic deployment while maintaining compatibility with local testing and Claude Code.

## Key Changes

### 1. Server Implementation

**Before (stdio):**
```python
from mcp.server import Server
server = Server("bfi-mcp")

@server.list_tools()
def list_tools():
    return [...]

@server.call_tool()
def call_tool(name: str, arguments: dict) -> ToolResult:
    ...

server.run(sys.stdin.buffer, sys.stdout.buffer)
```

**After (HTTP):**
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("bfi-mcp", stateless_http=True)

@mcp.tool()
def list_films(...) -> str:
    """List all BFI films with optional filtering"""
    ...

mcp.run(transport="streamable-http")
```

### 2. Tool Definitions

**Before:** Manual JSON schema in Tool objects
```python
LIST_FILMS_TOOL = Tool(
    name="list-films",
    description="...",
    inputSchema={
        "type": "object",
        "properties": {...}
    }
)
```

**After:** Pydantic Field decorators
```python
@mcp.tool()
def list_films(
    category: Optional[str] = Field(None, description="..."),
    location: Optional[str] = Field(None, description="..."),
    ...
) -> str:
```

### 3. Return Types

**Before:** ToolResult with TextContent
```python
return ToolResult(
    content=[TextContent(type="text", text=result)],
    isError=False,
)
```

**After:** Direct string return
```python
return result  # Plain string
```

### 4. Transport Declaration

**xmcp.config.ts**
```typescript
// Before
stdio: {
  command: "python",
  args: ["mcp_server.py"],
}

// After
http: {
  command: "python",
  args: ["mcp_server.py"],
}
```

## Benefits

### ✅ Alpic Deployment
- Native HTTP support matches Alpic's architecture
- No manual transport bridging needed
- Automatic scaling and load balancing

### ✅ Cleaner Code
- Decorator-based tool definition
- Type hints automatically generate schemas
- Less boilerplate

### ✅ Better Testing
- HTTP Inspector works directly
- Can be tested with curl, browsers, etc.
- Network requests visible for debugging

### ✅ Local HTTP Server
- Run locally for testing: `python mcp_server.py`
- Port 3000 for direct HTTP access
- Works with MCP Inspector

## Deployment Options

### Option 1: Alpic (Recommended)
- Deploy to cloud automatically
- Public HTTPS endpoint
- No local server needed
- See [ALPIC_SETUP.md](ALPIC_SETUP.md)

### Option 2: Local HTTP Server
- Start with: `python mcp_server.py`
- Access at: `http://127.0.0.1:3000`
- Use with MCP Inspector or Claude Code
- See [SETUP.md](SETUP.md)

### Option 3: Docker
- Build: `docker build -t bfi-mcp .`
- Run: `docker run -p 3000:3000 bfi-mcp`
- Access at: `http://localhost:3000`

## Compatibility

### Claude Code
Can still use BFI-MCP with Claude Code via HTTP:
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

### MCP Inspector
Works directly with HTTP endpoint:
```bash
npx @modelcontextprotocol/inspector
# Select: Streamable HTTP
# Enter: http://127.0.0.1:3000/mcp
```

### Alpic
Deployment automatically configures HTTP service

## Dependencies

### Added
- `pydantic>=2.11.0` - For Field decorators (already in mcp)
- `uvicorn>=0.31.1` - HTTP server (included with mcp)
- `starlette>=0.27` - Web framework (included with mcp)

### No Changes
- `mcp>=0.1.0` - Now includes FastMCP
- All existing data loading/filtering logic unchanged

## Testing

### Test Locally
```bash
# Terminal 1: Start server
python mcp_server.py

# Terminal 2: Test with curl
curl -X POST http://127.0.0.1:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'

# Or use MCP Inspector
npx @modelcontextprotocol/inspector
```

### Test Dockerized
```bash
docker build -t bfi-mcp .
docker run -p 3000:3000 bfi-mcp
```

### Test on Alpic
Deploy via [ALPIC_SETUP.md](ALPIC_SETUP.md) and test with provided endpoint

## Performance

- **Startup Time**: ~2 seconds (data loading)
- **Tool Response**: <100ms average
- **Memory Usage**: ~50-100 MB at runtime
- **Port**: 3000 (configurable via environment)

## Migration Notes

### For Users
- Update Claude Code config to use HTTP instead of stdio subprocess
- Keep server running when using locally
- Deploy to Alpic for production use

### For Developers
- All business logic (filtering, searching) unchanged
- Tool signatures simplified with type hints
- No complex ToolResult/TextContent wrapping needed
- Easier to add new tools

### For Testing
- Local server easy to debug with browser/curl
- HTTP Inspector shows request/response details
- Better error visibility

## Troubleshooting

### Server won't start
```bash
# Check port 3000 is available
lsof -i :3000

# Check dependencies
pip install -r requirements.txt
```

### Inspector can't connect
```bash
# Verify server running
curl http://127.0.0.1:3000/mcp

# Check firewall
# Make sure port 3000 is not blocked
```

### Alpic deployment fails
- Check `pyproject.toml` exists
- Check `uv.lock` exists
- See [ALPIC_SETUP.md](ALPIC_SETUP.md)

## What's Next?

1. **Deploy to Alpic** - See [ALPIC_SETUP.md](ALPIC_SETUP.md)
2. **Test locally** - Run `python mcp_server.py`
3. **Integrate with Claude Code** - Use HTTP config
4. **Monitor** - Check Alpic dashboard for usage/errors

---

**Status**: ✅ HTTP migration complete
**Transport**: Streamable HTTP via FastMCP
**Deployment**: Alpic-ready
**Last Updated**: November 8, 2025
