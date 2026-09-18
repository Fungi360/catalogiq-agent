"""MCP server for comparing small-business vendor catalogs."""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Vendor Catalog Comparison")

CATALOGS: dict[str, list[dict[str, Any]]] = {
    "holiday string lights": [
        {
            "vendor": "SunCo Supply",
            "product": "Commercial LED string lights",
            "unit_price": 18.50,
            "pack_size": "25 lights",
            "material": "weather-resistant PVC",
            "quality_score": 4.2,
        },
        {
            "vendor": "Seasonal Source",
            "product": "Commercial LED string lights",
            "unit_price": 16.75,
            "pack_size": "25 lights",
            "material": "indoor PVC",
            "quality_score": 3.6,
        },
        {
            "vendor": "Bright Wholesale",
            "product": "Commercial LED string lights",
            "unit_price": 21.00,
            "pack_size": "25 lights",
            "material": "weather-resistant PVC",
            "quality_score": 4.8,
        },
    ],
    "restaurant nitrile gloves": [
        {
            "vendor": "Kitchen Direct",
            "product": "Blue nitrile gloves",
            "unit_price": 12.00,
            "pack_size": "100 gloves",
            "material": "latex-free nitrile",
            "quality_score": 4.4,
        },
        {
            "vendor": "FoodSafe Supply",
            "product": "Blue nitrile gloves",
            "unit_price": 10.50,
            "pack_size": "100 gloves",
            "material": "latex-free nitrile",
            "quality_score": 4.0,
        },
    ],
    "brake pads": [
        {
            "vendor": "AutoParts Hub",
            "product": "Ceramic brake pads",
            "unit_price": 42.00,
            "pack_size": "1 axle set",
            "material": "ceramic composite",
            "quality_score": 4.5,
        },
        {
            "vendor": "Garage Wholesale",
            "product": "Ceramic brake pads",
            "unit_price": 38.00,
            "pack_size": "1 axle set",
            "material": "semi-metallic composite",
            "quality_score": 3.8,
        },
    ],
}


@mcp.tool()
def compare_vendor_catalogs(product_category: str) -> str:
    """Compare matching products across vendors on price, quality, and material."""
    category = product_category.strip().lower()
    products = CATALOGS.get(category)
    if not products:
        available = ", ".join(sorted(CATALOGS))
        return json.dumps(
            {"error": f"No catalog found for '{product_category}'.", "available_categories": available},
            indent=2,
        )

    best_value = min(products, key=lambda item: (item["unit_price"], -item["quality_score"]))
    highest_quality = max(products, key=lambda item: item["quality_score"])
    return json.dumps(
        {
            "product_category": category,
            "vendors": products,
            "recommendation": {
                "best_value_vendor": best_value["vendor"],
                "highest_quality_vendor": highest_quality["vendor"],
                "reason": (
                    f"{best_value['vendor']} has the lowest unit price at "
                    f"${best_value['unit_price']:.2f}; {highest_quality['vendor']} "
                    f"has the highest quality score at {highest_quality['quality_score']:.1f}."
                ),
            },
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
