# CatalogIQ: Vendor Catalog Comparison Agent

**Problem:** Small commercial buyers such as restaurants, auto repair shops, and seasonal retailers spend hours comparing the same product across multiple vendor catalogs, and existing tools compare price only, not quality or material.

## What the agent can do right now

- Accepts a plain-language request (for example, "Compare holiday string lights across the vendors.").
- Calls the `compare_vendor_catalogs` MCP tool over stdio, which returns every vendor's unit price, pack size, material, and quality score for that category.
- Names the lowest-price vendor and the highest-quality vendor separately and explains the material differences, using only the returned catalog data (model: `gpt-oss` on NRP).
- Returns the list of available categories when no catalog matches.

## Not implemented yet (intentional)

- Real vendor catalogs. The three categories (holiday string lights, restaurant nitrile gloves, brake pads) are hard-coded sample data.
- Uploading or parsing PDF, CSV, or spreadsheet catalogs.
- Spend tracking per vendor over time.
- Placing orders. The agent recommends; the buyer decides.

## Setup and run

1. Install Python 3.10 or newer.
2. Create a `.env` file in this folder:

```env
NRP_BASE_URL=https://your-nrp-endpoint.example/v1
NRP_API_KEY=your-api-key
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Run the agent (it starts the MCP server for you):

```bash
python vendor_catalog_agent.py "Compare holiday string lights across the vendors."
```

5. Run the tests (no API key needed):

```bash
python -m pytest -q
```

## Test cases

1. `holiday string lights` -> best value `Seasonal Source`; highest quality `Bright Wholesale`.
2. `restaurant nitrile gloves` -> best value `FoodSafe Supply`; highest quality `Kitchen Direct`.
3. `office chairs` (unknown category) -> error listing the available categories.

## Known limitations and bugs

1. Category matching is exact. "Holiday lights" or "string lights" returns an error, so results depend on the model passing the exact category name.
2. Quality scores are fixed sample values, not derived from reviews or specifications.
3. "Best value" is the lowest unit price only; it does not normalize for different pack sizes or weigh quality.

## Files

- `catalog_mcp_server.py`: FastMCP server and catalog comparison tool.
- `vendor_catalog_agent.py`: OpenAI Agents SDK agent connected to the MCP server.
- `test_catalog_mcp_server.py`: Three test cases with inputs and expected outputs.
