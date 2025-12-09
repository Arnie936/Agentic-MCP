# MCP All-in-One Server

This is a versatile MCP server that demonstrates multiple capabilities of the Model Context Protocol (MCP). It provides tools for calculation, external integrations (webhooks), resources for context, and prompt templates.

## Capabilities

### 🧮 Tools
Functions that the AI can execute:
- **Calculator**: Basic arithmetic operations (`add`, `subtract`, `multiply`, `divide`).
- **Webhook Integration**: `send_to_webhook` - Sends a text prompt to a configured n8n workflow and returns the response.

### 📚 Resources
Contextual data the AI can read:
- **`support://playbook`**: A full Customer Support Playbook containing company overview, tone rules, product details, and standard operating procedures.

### 📝 Prompts
Templates to structure AI interactions:
- **`webinar_to_blog`**: A structured prompt template to convert webinar transcripts into engaging blog posts.

## Prerequisites

- **Python 3.10+**
- **uv**: A fast Python package installer and resolver.
  - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js & npm** (optional, for the MCP Inspector)

## Setup

1. Open your terminal in this directory (`calculator_server`).
2. Initialize the project (if you haven't already):
   ```powershell
   uv init
   ```
3. Add the required dependencies:
   ```powershell
   uv add "mcp[cli]" httpx
   ```

## Running the Server

You can run the server directly using `uv`:

```powershell
uv run server.py
```

*Note: This will use stdio for communication, so it will expect input from stdin and won't show much output in the console unless connected to an MCP client.*

## Testing with MCP Inspector

To test the server using the MCP Inspector (a web-based tool to interact with your server):

```powershell
npx @modelcontextprotocol/inspector uv run server.py
```

This will launch the inspector in your browser. You can:
- **Tools**: Test the calculator and webhook tools.
- **Resources**: View the content of `support://playbook`.
- **Prompts**: Execute the `webinar_to_blog` template.

## Integration with Claude Desktop

To use this server with Claude for Desktop:

1. Open your Claude Desktop configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the server configuration. You can copy the content from `claude_desktop_config.json` in this directory:

   ```json
   {
     "mcpServers": {
       "calculator": {
         "command": "uv",
         "args": [
           "--directory",
           "C:\\Users\\Arnold\\Desktop\\mcps\\calculator_server",
           "run",
           "server.py"
         ]
       }
     }
   }
   ```

   **Important**: Make sure the path in `--directory` matches the actual absolute path to your `calculator_server` folder.

3. Restart Claude for Desktop.
