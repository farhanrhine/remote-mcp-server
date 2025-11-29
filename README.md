# Expense Tracker - Remote MCP Server

A remote MCP (Model Context Protocol) server for tracking expenses, built with FastMCP. This server can be accessed over HTTP, making it suitable for remote deployments and cloud hosting.

## 🌟 Features

- **Remote HTTP Server**: Accessible from any MCP client over the network
- **Async SQLite**: Non-blocking database operations with `aiosqlite`
- **Expense Tracking**: Add, list, and summarize expenses by category
- **Category Resources**: Predefined expense categories

## 📋 Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/farhanrhine/remote-mcp-server.git
cd remote-mcp-server

# Install dependencies
uv sync
```

## 🏃 Running the Server

### Option 1: Run as HTTP Server (Remote)

```bash
uv run python main.py
```

Server will be available at: `http://0.0.0.0:8000/mcp`

### Option 2: Using fastmcp command

```bash
uv run fastmcp run main.py --transport http --host 0.0.0.0 --port 8000
```

### Option 3: Run with MCP Inspector (Development)

**Terminal 1** - Start the server:
```bash
uv run python main.py
```

**Terminal 2** - Start the inspector:
```bash
uv run fastmcp dev main.py
```

### Option 4: Install to Claude Desktop (Local)

```bash
uv run fastmcp install claude-desktop main.py
```

## 📁 Project Structure

```
remote-mcp-server/
├── main.py              # MCP server with expense tracking tools
├── pyproject.toml       # Project dependencies
├── categories.json      # Custom expense categories (optional)
└── README.md            # This file
```

## 🛠️ MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_expense` | Add a new expense | `date`, `amount`, `category`, `subcategory`, `note` |
| `list_expenses` | List expenses in date range | `start_date`, `end_date` |
| `summarize` | Summarize by category | `start_date`, `end_date`, `category` (optional) |

## 📦 MCP Resources

| Resource URI | Description |
|--------------|-------------|
| `expense:///categories` | List of expense categories |

## 🔄 Run Commands Cheat Sheet

| Task | Command |
|------|---------|
| Run HTTP server | `uv run python main.py` |
| Run with fastmcp | `uv run fastmcp run main.py --transport http --host 0.0.0.0 --port 8000` |
| Run stdio mode | `uv run fastmcp run main.py` |
| Dev mode (Inspector) | `uv run fastmcp dev main.py` (requires server running first) |
| Install to Claude | `uv run fastmcp install claude-desktop main.py` |
| Add dependency | `uv add <package>` |
| Sync dependencies | `uv sync` |

## ⚙️ Transport Modes

| Mode | Command | Use Case |
|------|---------|----------|
| HTTP | `mcp.run(transport="http", host="0.0.0.0", port=8000)` | Remote access, cloud deployment |
| Streamable HTTP | `mcp.run(transport="streamable-http", ...)` | Streaming responses |
| stdio | `mcp.run()` or `mcp.run(transport="stdio")` | Local CLI clients (Claude Desktop) |

## 🔧 Configuration

### Database Location

The SQLite database is stored in the system's temp directory:
- **Windows**: `C:\Users\<user>\AppData\Local\Temp\expenses.db`
- **Linux/Mac**: `/tmp/expenses.db`

### Custom Categories

Create a `categories.json` file in the project root:

```json
{
  "categories": [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Bills & Utilities"
  ]
}
```

## 📚 Related Links

- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

## 📄 License

MIT
