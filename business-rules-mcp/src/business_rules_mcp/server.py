#!/usr/bin/env python3
"""FastMCP server for e-commerce business rules."""

import asyncio
import json
import logging
import sys

from mcp.server.fastmcp import FastMCP
from .rules_engine import RulesEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(name="business-rules")
rules_engine = RulesEngine()

# ==================== TOOLS ====================


@mcp.tool()
async def check_return_policy(
    category: str,
    days_since_purchase: int,
    opened: bool = False
) -> str:
    """Check if an item is eligible for return based on business rules.

    Args:
        category: Product category (electronics, clothing, books, food)
        days_since_purchase: Number of days since purchase
        opened: Whether the item has been opened
    """
    try:
        result = rules_engine.check_return_eligibility(category, days_since_purchase, opened)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error checking return policy: {str(e)}"


@mcp.tool()
async def calculate_shipping_cost(
    order_total: float,
    shipping_type: str = "standard"
) -> str:
    """Calculate shipping costs based on order total and type.

    Args:
        order_total: Total order amount in dollars
        shipping_type: Type of shipping (standard, expedited, express)
    """
    try:
        result = rules_engine.calculate_shipping(order_total, shipping_type)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error calculating shipping: {str(e)}"


@mcp.tool()
async def calculate_discount(
    customer_status: str = "existing",
    loyalty_tier: str = None,
    num_items: int = 1
) -> str:
    """Calculate applicable discounts for a customer.

    Args:
        customer_status: Customer status (new, existing)
        loyalty_tier: Loyalty tier (bronze, silver, gold)
        num_items: Number of items in order
    """
    try:
        result = rules_engine.calculate_discount(customer_status, loyalty_tier, num_items)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error calculating discount: {str(e)}"


@mcp.tool()
async def get_all_policies() -> str:
    """Get all business policies as a summary."""
    try:
        from .rules_engine import RETURN_POLICIES, SHIPPING_RULES, DISCOUNT_RULES

        policies = {
            "return_policies": RETURN_POLICIES,
            "shipping_rules": SHIPPING_RULES,
            "discount_rules": DISCOUNT_RULES,
        }
        return json.dumps(policies, indent=2)
    except Exception as e:
        return f"Error getting policies: {str(e)}"


# ==================== RESOURCES ====================


@mcp.resource("rules://return-policies")
async def return_policies_resource() -> str:
    """Access return policies as a resource."""
    from .rules_engine import RETURN_POLICIES
    return json.dumps({"return_policies": RETURN_POLICIES}, indent=2)


@mcp.resource("rules://shipping-rules")
async def shipping_rules_resource() -> str:
    """Access shipping rules as a resource."""
    from .rules_engine import SHIPPING_RULES
    return json.dumps({"shipping_rules": SHIPPING_RULES}, indent=2)


@mcp.resource("rules://discount-rules")
async def discount_rules_resource() -> str:
    """Access discount rules as a resource."""
    from .rules_engine import DISCOUNT_RULES
    return json.dumps({"discount_rules": DISCOUNT_RULES}, indent=2)


# ==================== SERVER LIFECYCLE ====================


async def startup() -> None:
    """Initialize on startup."""
    logger.info("Starting business rules MCP server...")


async def shutdown() -> None:
    """Cleanup on shutdown."""
    logger.info("Shutting down business rules MCP server...")


async def main() -> None:
    """Run the MCP server."""
    try:
        await startup()
        logger.info("Business rules MCP server running")
        await mcp.run_stdio_async()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        await shutdown()


if __name__ == "__main__":
    asyncio.run(main())
