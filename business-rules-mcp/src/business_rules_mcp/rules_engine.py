"""Business rules engine for e-commerce policies."""

from typing import Dict, Any
from datetime import datetime

# Hard-coded rules (could be database-backed in production)
RETURN_POLICIES = {
    "electronics": {"days": 14, "restocking_fee": 0.15},
    "clothing": {"days": 30, "restocking_fee": 0.0},
    "books": {"days": 60, "restocking_fee": 0.0},
    "food": {"days": 0, "restocking_fee": 0.0},  # No returns
}

SHIPPING_RULES = {
    "free_standard_threshold": 50.0,
    "free_expedited_threshold": 100.0,
    "express_fee": 15.0,
}

DISCOUNT_RULES = {
    "new_customer": 0.10,
    "bulk_tiers": [
        {"min_items": 5, "max_items": 10, "discount": 0.05},
        {"min_items": 11, "max_items": 20, "discount": 0.10},
        {"min_items": 21, "max_items": 999, "discount": 0.15},
    ],
    "loyalty_tiers": {
        "bronze": 0.05,
        "silver": 0.10,
        "gold": 0.15,
    },
}


class RulesEngine:
    """E-commerce business rules engine."""

    def check_return_eligibility(
        self, category: str, days_since_purchase: int, opened: bool = False
    ) -> Dict[str, Any]:
        """Check if item is eligible for return."""
        policy = RETURN_POLICIES.get(category.lower())

        if not policy:
            return {
                "eligible": False,
                "reason": f"Unknown category: {category}",
            }

        if policy["days"] == 0:
            return {
                "eligible": False,
                "reason": f"{category.title()} items cannot be returned",
            }

        if days_since_purchase > policy["days"]:
            return {
                "eligible": False,
                "reason": f"Return window expired ({policy['days']} days)",
            }

        restocking_fee = policy["restocking_fee"] if opened else 0.0

        return {
            "eligible": True,
            "days_remaining": policy["days"] - days_since_purchase,
            "restocking_fee_percent": restocking_fee * 100,
            "refund_method": "original_payment",
        }

    def calculate_shipping(self, order_total: float, shipping_type: str = "standard") -> Dict[str, Any]:
        """Calculate shipping costs based on order total."""
        if order_total >= SHIPPING_RULES["free_expedited_threshold"]:
            return {
                "cost": 0.0,
                "type": "expedited",
                "message": "Free expedited shipping (order > $100)",
            }

        if order_total >= SHIPPING_RULES["free_standard_threshold"]:
            return {
                "cost": 0.0,
                "type": "standard",
                "message": "Free standard shipping (order > $50)",
            }

        if shipping_type == "express":
            return {
                "cost": SHIPPING_RULES["express_fee"],
                "type": "express",
                "message": "Express shipping (next-day delivery)",
            }

        return {
            "cost": 5.99,
            "type": "standard",
            "message": "Standard shipping (3-5 business days)",
        }

    def calculate_discount(
        self,
        customer_status: str = "existing",
        loyalty_tier: str = None,
        num_items: int = 1
    ) -> Dict[str, Any]:
        """Calculate applicable discounts."""
        discounts = []
        total_discount = 0.0

        # New customer discount
        if customer_status == "new":
            discounts.append({
                "type": "new_customer",
                "amount": DISCOUNT_RULES["new_customer"],
                "description": "10% off first order",
            })
            total_discount += DISCOUNT_RULES["new_customer"]

        # Loyalty tier discount
        if loyalty_tier and loyalty_tier.lower() in DISCOUNT_RULES["loyalty_tiers"]:
            amount = DISCOUNT_RULES["loyalty_tiers"][loyalty_tier.lower()]
            discounts.append({
                "type": "loyalty",
                "amount": amount,
                "description": f"{loyalty_tier.title()} member discount",
            })
            total_discount += amount

        # Bulk order discount
        for tier in DISCOUNT_RULES["bulk_tiers"]:
            if tier["min_items"] <= num_items <= tier["max_items"]:
                discounts.append({
                    "type": "bulk",
                    "amount": tier["discount"],
                    "description": f"Bulk order discount ({num_items} items)",
                })
                total_discount += tier["discount"]
                break

        # Cap at 25% total discount
        total_discount = min(total_discount, 0.25)

        return {
            "applicable_discounts": discounts,
            "total_discount_percent": total_discount * 100,
            "max_discount_reached": total_discount >= 0.25,
        }
