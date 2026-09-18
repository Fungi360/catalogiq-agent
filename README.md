# Vendor Catalog Comparison Agent

An AI-powered catalog intelligence agent that retrieves, compares, and ranks products across multiple sources using company-specific knowledge, pricing, specifications, and quality criteria.

This project currently implements the Team 9 Milestone 1 use case: helping small commercial buyers compare products from multiple vendor catalogs on price, quality, and material composition.

## Requirements

- Python 3.10+
- An NRP OpenAI-compatible endpoint with `NRP_BASE_URL` and `NRP_API_KEY`
- Dependencies from `requirements.txt`

Create a `.env` file in this folder:

```env
NRP_BASE_URL=https://your-nrp-endpoint.example/v1
NRP_API_KEY=your-api-key
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the MCP server directly

The server is normally started automatically by the agent over stdio. To verify the server starts:

```powershell
python catalog_mcp_server.py
```

## Run the agent

```powershell
python vendor_catalog_agent.py "Compare holiday string lights across the vendors."
```

The agent connects to `catalog_mcp_server.py` through `MCPServerStdio` and calls the `compare_vendor_catalogs` MCP tool before responding.

## Tests

The three deterministic test cases verify the MCP tool without requiring an API key:

```powershell
python -m pytest -q
```

Test inputs and expected outputs:

1. `holiday string lights` -> lowest-price vendor `Seasonal Source`; highest-quality vendor `Bright Wholesale`.
2. `restaurant nitrile gloves` -> lowest-price vendor `FoodSafe Supply`; highest-quality vendor `Kitchen Direct`.
3. `unknown category` -> an error response listing the available categories.

## Files

- `catalog_mcp_server.py`: FastMCP server and catalog comparison tool.
- `vendor_catalog_agent.py`: OpenAI Agents SDK agent connected to the MCP server.
- `test_catalog_mcp_server.py`: Three test cases with inputs and expected outputs.
