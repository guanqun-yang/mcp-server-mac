# Local Deployment Guide for MCP Server Mac

This guide provides step-by-step instructions for deploying the MCP Server Mac locally with Claude Desktop.

## Prerequisites

- Python 3.12+ installed
- Claude Desktop application
- Docker (for containerized deployment)
- Git (to clone/manage the repository)

## Deployment Option 1: Direct Installation on Same Machine

### Step 1: Install the MCP Server

1. Navigate to the project directory:
   ```bash
   cd /path/to/mcp-server-mac
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

3. Verify installation:
   ```bash
   mcp-server-mac --help
   ```

### Step 2: Configure Claude Desktop

1. Locate your Claude Desktop configuration file:
   - **Linux**: `~/.config/claude-desktop/config.json`
   - **macOS**: `~/Library/Application Support/Claude/config.json`
   - **Windows**: `%APPDATA%\Claude\config.json`

2. Edit the configuration file to add the MCP server:
   ```json
   {
     "mcp": {
       "servers": {
         "mcp-server-mac": {
           "command": "mcp-server-mac",
           "transport": "stdio"
         }
       }
     }
   }
   ```

3. Save the file and restart Claude Desktop.

### Step 3: Test the Connection

1. Open Claude Desktop
2. Start a new conversation
3. The MCP server should automatically connect
4. Test by asking Claude to get the MAC address using the available tool

---

## Deployment Option 2: Containerized on Same Machine

### Step 1: Build the Docker Image

1. Navigate to the project directory:
   ```bash
   cd /path/to/mcp-server-mac
   ```

2. Build the Docker image:
   ```bash
   docker build -t mcp-server-mac .
   ```

### Step 2: Run the Container

1. Start the container with HTTP transport:
   ```bash
   docker run -d \
     --name mcp-server-mac \
     -p 8000:8000 \
     -e MCP_TRANSPORT=streamable-http \
     -e HOST=0.0.0.0 \
     -e PORT=8000 \
     mcp-server-mac
   ```

2. Verify the container is running:
   ```bash
   docker ps
   ```

3. Check container logs:
   ```bash
   docker logs mcp-server-mac
   ```

### Step 3: Configure Claude Desktop for HTTP Transport

1. Edit your Claude Desktop configuration file:
   ```json
   {
     "mcp": {
       "servers": {
         "mcp-server-mac": {
           "url": "http://localhost:8000",
           "transport": "http"
         }
       }
     }
   }
   ```

2. Save the file and restart Claude Desktop.

### Step 4: Test the Connection

1. Open Claude Desktop
2. Start a new conversation
3. The MCP server should connect via HTTP
4. Test by asking Claude to get the MAC address using the available tool

---

## Troubleshooting

### Common Issues

1. **MCP server not found**
   - Ensure the package is properly installed: `pip list | grep mcp-server-mac`
   - Try using the full path to the executable in the config

2. **Connection refused (containerized)**
   - Check if the container is running: `docker ps`
   - Verify port mapping: `docker port mcp-server-mac`
   - Check firewall settings

3. **Claude Desktop not recognizing the server**
   - Verify the config.json syntax is valid
   - Check Claude Desktop logs for error messages
   - Restart Claude Desktop after configuration changes

### Logs and Debugging

- **Container logs**: `docker logs mcp-server-mac`
- **Claude Desktop logs**: Check application logs in system log viewer
- **Test HTTP endpoint**: `curl http://localhost:8000/health` (if health endpoint is available)

### Managing the Container

```bash
# Stop the container
docker stop mcp-server-mac

# Start the container
docker start mcp-server-mac

# Remove the container
docker rm mcp-server-mac

# Rebuild and restart
docker stop mcp-server-mac
docker rm mcp-server-mac
docker build -t mcp-server-mac .
docker run -d --name mcp-server-mac -p 8000:8000 -e MCP_TRANSPORT=streamable-http mcp-server-mac
```

---

## Available Tools

Once successfully deployed, the MCP server provides the following tool:

- **get_mac_address**: Returns the MAC address of the machine where the server is running

## Environment Variables

The server supports the following environment variables:

- `MCP_TRANSPORT`: Transport method (`stdio` or `streamable-http`)
- `HOST`: Host to bind to (default: `0.0.0.0`)
- `PORT`: Port to listen on (default: `8000`)