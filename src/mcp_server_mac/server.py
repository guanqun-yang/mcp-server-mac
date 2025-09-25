from mcp.server.fastmcp import FastMCP
import os
import uuid

# Configure FastMCP with proper host binding for containers
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))

mcp = FastMCP("mcp_server_mac", host=host, port=port)

@mcp.tool()
async def get_mac_address() -> str:
    """Return the MAC address of the current machine."""
    mac = uuid.getnode()
    mac_str = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))
    return mac_str

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()