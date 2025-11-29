from fastmcp import FastMCP

# Create a proxy to your remote FastMCP Cloud server so used as a local server
# FastMCP Cloud uses Streamable HTTP (default), so just use the /mcp URL
mcp = FastMCP.as_proxy(
    "https://red-arm.fastmcp.app/mcp",  # Standard FastMCP Cloud URL
    name="Farhan Proxy v1.0"  # Optional: Name your proxy server"
)

if __name__ == "__main__":
    # This runs via STDIO, which Claude Desktop can connect to
    mcp.run()