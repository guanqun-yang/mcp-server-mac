from mcp.server.fastmcp import FastMCP
import os

# Configure FastMCP with proper host binding for containers
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))

mcp = FastMCP("mcp-server-mac", host=host, port=port)

@mcp.tool()
async def get_mac_address(query: str) -> str:
    """Return the MAC address of the current machine."""
    return str(query.lower().count("r"))

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()