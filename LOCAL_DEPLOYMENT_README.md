# MCP Server Local Deployment Guide

This guide explains how to deploy the MCP server on a remote Ubuntu server and connect to it from your MacBook Pro.

## Architecture Overview

- **Remote Ubuntu Server**: `192.168.1.254` - Runs the MCP server
- **MacBook Pro**: Your local machine - Runs Claude Code and connects to the remote server
- **Transport**: HTTP with Server-Sent Events (SSE)
- **Port**: 8000

## Setup Instructions

### Part 1: Remote Ubuntu Server Setup (192.168.1.254)

#### 1. Install Dependencies

```bash
# Navigate to the project directory
cd /path/to/mcp-server-mac

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

#### 2. Configure Firewall (if needed)

```bash
# Allow incoming connections on port 8000
sudo ufw allow 8000

# Check firewall status
sudo ufw status
```

#### 3. Start the MCP Server

```bash
# Start the server with HTTP transport
MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 mcp-server-mac
```

**Alternative using environment variables:**
```bash
export MCP_TRANSPORT=streamable-http
export HOST=0.0.0.0
export PORT=8000
mcp-server-mac
```

#### 4. Verify Server is Running

```bash
# Test local connection
curl -v http://localhost:8000/mcp
# Should return: "Not Acceptable: Client must accept text/event-stream"
# This is expected - it means the SSE endpoint is working correctly

# Check if server is listening on all interfaces
ss -tuln | grep 8000
```

#### 5. Keep Server Running (Optional)

For permanent deployment, use one of these methods:

**Option A: Using screen/tmux**
```bash
screen -S mcp-server
MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 mcp-server-mac
# Press Ctrl+A, then D to detach
```

**Option B: Using nohup**
```bash
nohup env MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 mcp-server-mac > mcp-server.log 2>&1 &
```

### Part 2: MacBook Pro Setup (Client)

#### 1. Add the Remote MCP Server

```bash
# Add the server configuration
claude mcp add --transport http mac-server http://192.168.1.254:8000/mcp
```

#### 2. Verify Configuration

```bash
# List all configured MCP servers
claude mcp list

# Get details for the specific server
claude mcp get mac-server
```

#### 3. Test the Connection

```bash
# Start Claude Code and the server should be available
claude
```

In Claude Code, you should now be able to use the `get_mac_address` tool that returns the MAC address of the Ubuntu server.

## Troubleshooting

### Server Issues

**Server won't start:**
- Check if port 8000 is already in use: `ss -tuln | grep 8000`
- Verify dependencies are installed: `pip list | grep mcp`

**Connection refused:**
- Ensure firewall allows port 8000: `sudo ufw allow 8000`
- Check server is binding to 0.0.0.0, not just localhost
- Verify server process is running: `ps aux | grep mcp-server`

### Client Issues

**Cannot connect from MacBook:**
- Test network connectivity: `ping 192.168.1.254`
- Test port connectivity: `telnet 192.168.1.254 8000`
- Verify server URL is correct: `http://192.168.1.254:8000/mcp`

**Server not listed in Claude Code:**
- Check MCP configuration: `claude mcp list`
- Remove and re-add server if needed: `claude mcp remove mac-server`

## Server Management

### Stop the Server
```bash
# Find the process ID
ps aux | grep mcp-server

# Kill the process
kill <PID>
```

### View Server Logs
```bash
# If running with nohup
tail -f mcp-server.log

# If running in screen
screen -r mcp-server
```

### Update the Server
```bash
# Pull latest changes
git pull

# Reinstall package
pip install -e .

# Restart server
# (kill existing process and start new one)
```

## Security Considerations

- The server is exposed on your local network (192.168.1.254:8000)
- Consider using authentication if needed
- Use firewall rules to restrict access if required
- For production use, consider HTTPS/TLS encryption

## Server Configuration

The server configuration is controlled by environment variables:
- `MCP_TRANSPORT`: Set to "streamable-http" for HTTP transport
- `HOST`: Set to "0.0.0.0" to accept external connections
- `PORT`: Set to "8000" (or any available port)

## Available Tools

Once connected, the following MCP tools will be available in Claude Code:
- `get_mac_address`: Returns the MAC address of the Ubuntu server