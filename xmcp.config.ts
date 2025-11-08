/**
 * BFI-MCP Server Configuration
 * Transport: stdio (standard input/output for Claude Code integration)
 */

export default {
  stdio: {
    command: "python",
    args: ["mcp_server.py"],
  },
};
