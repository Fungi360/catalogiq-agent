"""Acceptance tests for the vendor catalog MCP tool."""

import json

from catalog_mcp_server import compare_vendor_catalogs


def test_holiday_lights_recommendation() -> None:
    result = json.loads(compare_vendor_catalogs("holiday string lights"))
    assert result["recommendation"]["best_value_vendor"] == "Seasonal Source"
    assert result["recommendation"]["highest_quality_vendor"] == "Bright Wholesale"


def test_restaurant_gloves_recommendation() -> None:
    result = json.loads(compare_vendor_catalogs("restaurant nitrile gloves"))
    assert result["recommendation"]["best_value_vendor"] == "FoodSafe Supply"
    assert result["recommendation"]["highest_quality_vendor"] == "Kitchen Direct"


def test_unknown_category_lists_available_inputs() -> None:
    result = json.loads(compare_vendor_catalogs("office chairs"))
    assert result["error"] == "No catalog found for 'office chairs'."
    assert "holiday string lights" in result["available_categories"]
