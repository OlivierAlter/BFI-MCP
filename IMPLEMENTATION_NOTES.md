# BFI-MCP Implementation Analysis

Comparison with alpic-ai's MCP Server Template and verification against MCP SDK best practices.

## Overview

Our implementation is **correct for Claude Code integration** but uses an older MCP SDK pattern compared to the alpic template. This is intentional and appropriate for our use case.

## Key Differences

### 1. Transport Type

| Aspect | Our Implementation | Alpic Template |
|--------|-------------------|----------------|
| **Transport** | `stdio` (stdin/stdout) | `streamable-http` (port 3000) |
| **Use Case** | Claude Code subprocess | Web-accessible API |
| **Communication** | Direct process pipes | HTTP over network |
| **Port** | None (subprocess) | 3000 |

**Verdict**: ✅ Our choice is **correct for Claude Code**. Claude Code calls MCPs as subprocesses and communicates via stdio.

### 2. Server Implementation Pattern

| Aspect | Our Implementation | Alpic Template |
|--------|-------------------|----------------|
| **Class** | `Server` (older pattern) | `FastMCP` (newer pattern) |
| **Tool Definition** | Manual `Tool()` objects | `@mcp.tool()` decorator |
| **List Tools** | `@server.list_tools()` | Auto-generated from decorators |
| **Call Tool** | `@server.call_tool()` | Auto-dispatched to decorated functions |
| **Code Style** | Explicit/verbose | Implicit/concise |

**Analysis**: Our implementation works perfectly but uses the older `Server` class API. The `FastMCP` pattern is newer and cleaner but requires the same underlying MCP SDK.

### 3. MCP SDK Version

Both use `mcp>=0.1.0`. Our implementation is compatible with:
- ✅ Anthropic MCP SDK (current as of Nov 2025)
- ✅ Claude Code integration
- ✅ Manual tool definition via `Tool()` objects
- ✅ stdio transport via `server.run(stdin, stdout)`

## Code Pattern Comparison

### Their Pattern (FastMCP - Simpler)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server Name")

@mcp.tool()
def my_tool(param: str) -> str:
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Pros:**
- Clean, decorator-based API
- Automatic parameter extraction via type hints
- Less boilerplate code

**Cons:**
- Less explicit (harder to debug tool definitions)
- Limited for complex return types

### Our Pattern (Server - Explicit)

```python
from mcp.server import Server
from mcp.types import Tool, ToolResult

server = Server("Server Name")

LIST_TOOL = Tool(
    name="list",
    description="...",
    inputSchema={...}
)

@server.list_tools()
def list_tools():
    return [LIST_TOOL]

@server.call_tool()
def call_tool(name: str, arguments: dict) -> ToolResult:
    # Tool implementation

if __name__ == "__main__":
    server.run(sys.stdin.buffer, sys.stdout.buffer)
```

**Pros:**
- Explicit tool definitions (easier to audit)
- Full control over JSON schemas
- Complex return types handled explicitly via `ToolResult`

**Cons:**
- More boilerplate code
- Requires manual tool registration

## Transport Type Deep Dive

### Why We Use stdio (Correct for Claude Code)

Claude Code calls MCPs as **subprocesses** using this pattern:

```json
{
  "mcps": {
    "bfi": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

When Claude Code invokes the MCP:
1. Spawns process: `python mcp_server.py`
2. Opens stdin/stdout pipes
3. Communicates via stdio (MCP messages)
4. Closes process when done

Our code correctly handles this:
```python
server.run(sys.stdin.buffer, sys.stdout.buffer)
```

### Why Alpic Uses streamable-http

The alpic template is designed for:
- Network-accessible MCP servers
- Long-running processes on port 3000
- Remote integration (not local subprocess)

For their use case, HTTP makes sense. For Claude Code, stdio is correct.

## Verification Checklist

✅ **Transport**: stdio is correct for Claude Code subprocess integration
✅ **Tool Definition**: Explicit `Tool()` objects are valid MCP SDK pattern
✅ **Tool Registration**: `@server.list_tools()` and `@server.call_tool()` decorators are correct
✅ **Input Validation**: Using JSON Schema in `inputSchema` is standard MCP practice
✅ **Return Type**: `ToolResult` with `TextContent` is correct for text responses
✅ **Error Handling**: Try-catch in `call_tool()` is appropriate
✅ **Data Loading**: Loading at startup before `server.run()` is correct
✅ **Dependencies**: Using `mcp>=0.1.0` is appropriate

## Why NOT to Switch to FastMCP

While FastMCP is newer and cleaner, switching would provide no benefit for our use case:

1. **Different Transport**: FastMCP examples show `streamable-http`, not stdio
2. **Same SDK**: Both use the same underlying MCP SDK
3. **Working Code**: Our implementation is proven to work with Claude Code
4. **Explicit Control**: Our verbose pattern gives better control for complex tools
5. **Debugging**: Explicit schemas are easier to debug than implicit decorators

## Recommendations

### Keep Current Implementation? ✅ YES

Our implementation is:
- ✅ Correct for Claude Code (stdio transport)
- ✅ Following valid MCP SDK patterns
- ✅ Proven to work (tests passing)
- ✅ Explicit and auditable
- ✅ Properly documented

### When to Consider FastMCP?

Only if you:
- Switch to HTTP-based MCP servers
- Want to run the MCP as a long-running network service
- Prefer decorator-based implicit patterns
- Need streamable-http or SSE transport

For Claude Code integration, our approach is optimal.

## xmcp.config.ts Purpose

We added `xmcp.config.ts` for CodeBuild compatibility:

```typescript
export default {
  stdio: {
    command: "python",
    args: ["mcp_server.py"],
  },
};
```

This explicitly declares our stdio transport for build systems. It's not required for Claude Code but helps automated build/deployment pipelines detect MCP configuration.

## Summary

**Our Implementation: ✅ CORRECT AND OPTIMAL**

- Uses stdio transport (correct for Claude Code)
- Uses valid MCP SDK `Server` class pattern
- Properly handles tool definition and dispatch
- Explicitly manages complex return types
- All tests passing
- Ready for production Claude Code integration

**No changes needed.** Our approach is a valid, well-supported MCP SDK pattern that's perfectly suited for Claude Code integration.

---

**Reference**:
- [MCP SDK Documentation](https://modelcontextprotocol.io/)
- [Claude Code MCP Integration](https://docs.claude.com/en/docs/claude-code/mcp)
- Alpic MCP Template: https://github.com/alpic-ai/mcp-server-template-python

**Last Verified**: November 8, 2025
**Status**: ✅ Verified Against Latest MCP Standards
