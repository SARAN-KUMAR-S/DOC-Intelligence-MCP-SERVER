# DOC-Intelligence-MCP-SERVER

A Model Context Protocol (MCP) server that enables LLMs (like Claude) to dynamically search, scrape, and query libraries' official documentation using Google Serper and Groq.

## Features

- **Google Serper API Integration:** Searches documentation sites for up-to-date information.
- **Fast Web Scraping:** Extracts page content cleanly using `trafilatura`.
- **LLM Content Cleaning:** Automatically cleans and strips HTML bloat from documentation pages using Groq (`llama-3.1-8b-instant`).
- **Claude Integration:** Instantly works as a tool within Claude Desktop or any other MCP client.

## Supported Libraries (Configured Domains)
- `uv` (docs.astral.sh/uv)
- `openai` (platform.openai.com/docs)
- `langchain` (python.langchain.com/docs)
- `llama-index` (docs.llamaindex.ai/en/stable)

---

## Setup

### 1. Requirements
Ensure you have [uv](https://docs.astral.sh/uv/) installed.

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
Inside `.env`:
- `SERPER_API_KEY`: Get one from [Serper.dev](https://serper.dev/)
- `GROQ_API_KEY`: Get one from [Groq Console](https://console.groq.com/)

### 3. Run Locally (Testing)
You can run the test client to verify operations:
```bash
uv run client.py
```

---

## Claude Desktop Integration

To add this tool to your Claude Desktop client, edit your configuration file:

* **Windows Path:** `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS Path:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Choose one of the integration methods below:

### Option 1: Run directly from GitHub (Quickest, no cloning required)
This runs the MCP server directly from GitHub. Add this JSON snippet under `"mcpServers"`:

```json
{
  "mcpServers": {
    "docs-intelligence": {
      "command": "uv",
      "args": [
        "run",
        "https://raw.githubusercontent.com/SARAN-KUMAR-S/DOC-Intelligence-MCP-SERVER/main/mcp_server.py"
      ],
      "env": {
        "SERPER_API_KEY": "YOUR_SERPER_API_KEY",
        "GROQ_API_KEY": "YOUR_GROQ_API_KEY"
      }
    }
  }
}
```

> [!IMPORTANT]
> Replace `YOUR_SERPER_API_KEY` and `YOUR_GROQ_API_KEY` with your actual credentials.

### Option 2: Clone and Run Locally (Best for making code changes)
If you cloned the repository locally, create a `.env` file containing your API keys in the root directory, and configure the path under `"mcpServers"`:

```json
{
  "mcpServers": {
    "docs-intelligence": {
      "command": "uv",
      "args": [
        "--directory",
        "ABSOLUTE_PATH_TO_CLONED_FOLDER",
        "run",
        "mcp_server.py"
      ]
    }
  }
}
```
> [!NOTE]
> Replace `ABSOLUTE_PATH_TO_CLONED_FOLDER` with the full path where you cloned this repository (e.g. `C:\\Users\\Username\\DOC-Intelligence-MCP-SERVER`). The local `.env` file in that folder will be loaded automatically.

---

Restart Claude Desktop, and the `get_docs` tool will be ready to use!

