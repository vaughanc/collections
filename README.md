# 🗑️ Reading Bin Collections MCP Server

**An MCP-compliant tool for fetching household waste collection dates from Reading Borough Council.**  
Built for seamless integration with Claude.

![InitialPrompt](screenshots/InitialPrompt.png?raw=true "InitialPrompt")
![Results](screenshots/Results.png?raw=true "Results")

---

## 🔧 What it Does

This MCP server allows you to ask questions like:

> *“What are my bin collections for 51 Gosbrook Road, RG48BN?”*

…directly within Claude. It looks up the postcode and house number via Reading Borough Council's API and returns your upcoming collection dates.

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/vaughanc/collections.git
```
### 2. Install UV

```
curl -LsSf https://astral.sh/uv/install.sh | sh

```
Make sure to restart your terminal afterwards to ensure that the uv command gets picked up.

### 3. Create a virtual environment

```
uv init collections
uv venv                                                   
source .venv/bin/activate
uv run fastmcp install --with uvicorn --with requests collections.py
```

The install command will create the config for Claude to detect the MCP server.

You can check this in the following file
```

cat  ~/Library/Application\ Support/Claude/claude_desktop_config.json 
{
  "mcpServers": {
    "Reading Bin Collections Tool": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "requests",
        "--with",
        "uvicorn",
        "fastmcp",
        "run",
        "/Users/chris/Documents/Code/collections/collections.py"
      ]
    }
    }
  }

```
When you start Claude you should see the following 

![Claude Prompt and Menu Item](screenshots/PromptandMenuItem.png?raw=true "Claude prompt and menu item")


📬 API Behind the Scenes

This tool makes two key requests:

1. Get address UPRN

Endpoint: https://www.reading.gov.uk/api/address-search
Params: postcode
Use: Resolves a UPRN for a given street/postcode.

2. Fetch collection schedule

Endpoint: https://www.reading.gov.uk/api/bin-collections
Params: uprn
Use: Retrieves bin types and dates (recycling, food waste, domestic, etc.)

📸 Screenshots

![InitialPrompt](screenshots/InitialPrompt.png?raw=true "InitialPrompt")
![PromptandMenuItem](screenshots/PromptandMenuItem.png?raw=true "PromptandMenuItem")
![ExternalIntegrationApproval](screenshots/ExternalIntegrationApproval.png?raw=true "ExternalIntegrationApproval")
![Request](screenshots/Request.png?raw=true "Request")
![Results](screenshots/Results.png?raw=true "Results")


I used this quickstart guide to provide the background to get going.

https://modelcontextprotocol.io/quickstart/server

I also may have used brew to resolve some dependencies such as NPM but can't recall.

https://brew.sh/
