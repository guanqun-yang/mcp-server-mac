# MCP Server Mac - Deployment Guide

This MCP server returns the MAC address of the machine where it's running. This guide covers three deployment methods for use with Claude Desktop.

## Claude Desktop Connection Requirements

**Understanding Transport Types:**
- **stdio**: Local process communication via standard input/output
- **streamable-http**: HTTP-based communication for remote servers
- **SSE**: Server-Sent Events (being deprecated)

**Claude Desktop Constraints:**
- **Local servers**: Must use `stdio` transport via `claude_desktop_config.json`
- **Remote servers**: Must use `streamable-http` via Settings > Connectors web interface
- **Configuration structure**: Must use `mcpServers` with mandatory `command` field
- **Plan requirement**: Remote servers require Claude Pro/Team/Enterprise plans

---

## Method 1: Fully Remote Deployment

Deploy the MCP server on a remote server or cloud platform, accessible via public URL.

### Using Smithery.AI or Similar Platforms

1. **Deploy to a cloud platform:**
   ```bash
   # Example using Smithery.AI, Railway, or similar
   # Follow platform-specific deployment instructions
   # Ensure the server runs with streamable-http transport
   ```

2. **Configure Claude Desktop:**
   - Navigate to https://claude.ai/settings/integrations
   - Click "Add Connector"
   - Enter your server URL: `https://your-server.smithery.ai`
   - The server automatically uses `streamable-http` transport

3. **Server Configuration (for remote deployment):**
   ```python
   # Ensure your server.py is configured for HTTP transport
   mcp = FastMCP("mcp_server_mac", host="0.0.0.0", port=8000)

   def main():
       mcp.run(transport="streamable-http")
   ```

### Benefits:
- ✅ True `streamable-http` connection
- ✅ Works with Claude Desktop's native remote server support
- ✅ No local configuration needed
- ✅ Accessible from anywhere

### Requirements:
- Public server/cloud platform
- Claude Pro/Team/Enterprise plan
- Server accessible via HTTPS

---

## Method 2: Fully Local Deployment (No Docker)

Install and run the MCP server directly on your local machine.

### Prerequisites
- Python 3.12+
- Claude Desktop application

### Installation Steps

1. **Install the MCP server:**
   ```bash
   cd /path/to/mcp-server-mac
   pip install -e .
   ```

2. **Verify installation:**
   ```bash
   mcp-server-mac --help
   ```

3. **Configure Claude Desktop:**

   Edit your Claude Desktop configuration file:
   - **Linux**: `~/.config/claude-desktop/config.json`
   - **macOS**: `~/Library/Application Support/Claude/config.json`
   - **Windows**: `%APPDATA%\Claude\config.json`

   ```json
   {
     "mcpServers": {
       "mcp-server-mac": {
         "command": "mcp-server-mac",
         "transport": "stdio"
       }
     }
   }
   ```

   **For conda environments, use the full path:**
   ```json
   {
     "mcpServers": {
       "mcp-server-mac": {
         "command": "/opt/anaconda3/envs/mcp-server-mac/bin/mcp-server-mac",
         "transport": "stdio"
       }
     }
   }
   ```

4. **Restart Claude Desktop and test the connection.**

### Benefits:
- ✅ Simple setup
- ✅ No Docker complexity
- ✅ Direct local execution
- ✅ Works with free Claude Desktop

### Transport Type:
- Uses `stdio` transport (not `streamable-http`)

---

## Method 3: Local Docker Deployment

Run the MCP server in a Docker container with two connection options.

### Build and Run Container

1. **Build the Docker image:**
   ```bash
   cd /path/to/mcp-server-mac
   docker build -t mcp-server-mac .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name mcp-server-mac \
     -p 8000:8000 \
     -e MCP_TRANSPORT=streamable-http \
     -e HOST=0.0.0.0 \
     -e PORT=8000 \
     mcp-server-mac
   ```

### Option 3A: Script-Based Connection (stdio)

Connect via a wrapper script using `stdio` transport.

1. **Create wrapper script `mcp-server-mac-container.sh`:**
   ```bash
   #!/bin/bash
   docker exec mcp-server-mac mcp-server-mac
   ```

2. **Make executable:**
   ```bash
   chmod +x mcp-server-mac-container.sh
   ```

3. **Configure Claude Desktop:**
   ```json
   {
     "mcpServers": {
       "mcp-server-mac": {
         "command": "/path/to/mcp-server-mac-container.sh",
         "transport": "stdio"
       }
     }
   }
   ```

**Transport Type:** `stdio` (not true `streamable-http`)

### Option 3B: Public URL with ngrok (streamable-http)

Expose the container via public URL for true HTTP connection.

1. **Install and run ngrok:**
   ```bash
   # Install ngrok
   ngrok http 8000
   ```

2. **Configure Claude Desktop:**
   - Navigate to https://claude.ai/settings/integrations
   - Add connector with ngrok URL: `https://xyz123.ngrok-free.app`
   - Requires Claude Pro/Team/Enterprise plan

**Transport Type:** True `streamable-http`

### Container Management

```bash
# Stop container
docker stop mcp-server-mac

# Start container
docker start mcp-server-mac

# View logs
docker logs mcp-server-mac

# Remove container
docker rm mcp-server-mac
```

---

## Troubleshooting

### Common Issues

1. **MCP server not found**
   - Use full absolute path to executable
   - For conda: `/opt/anaconda3/envs/mcp-server-mac/bin/mcp-server-mac`
   - Verify installation: `pip list | grep mcp-server-mac`

2. **Invalid JSON configuration**
   - Use `mcpServers` structure (not `mcp.servers`)
   - `command` field is mandatory
   - Validate JSON syntax

3. **Container connection issues**
   - Ensure container is running: `docker ps`
   - Test wrapper script: `./mcp-server-mac-container.sh --help`
   - For ngrok: verify public URL is accessible

4. **Claude Desktop not recognizing server**
   - Restart Claude Desktop after config changes
   - Check logs for error messages
   - Verify executable permissions

### Transport Type Summary

| Method | Transport Type | Claude Desktop Config |
|--------|----------------|----------------------|
| Remote deployment | `streamable-http` | Settings > Connectors |
| Local installation | `stdio` | `claude_desktop_config.json` |
| Docker + script | `stdio` | `claude_desktop_config.json` |
| Docker + ngrok | `streamable-http` | Settings > Connectors |

---

## Available Tools

Once deployed, the MCP server provides:

- **get_mac_address**: Returns the MAC address of the machine where the server is running

## Environment Variables

- `MCP_TRANSPORT`: `stdio` or `streamable-http`
- `HOST`: Host to bind to (default: `0.0.0.0`)
- `PORT`: Port to listen on (default: `8000`)