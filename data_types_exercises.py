"""Small demonstrations of Python's built-in collection types.

The examples cover log parsing, aggregate calculations, set operations, and
filtering structured product data.
"""

from typing import Any


def analyze_damage(hits: list[int]) -> tuple[int, float, int]:
    """Return the total, average, and largest value in a list of hits."""
    if not hits:
        return 0, 0.0, 0

    total = sum(hits)
    return total, total / len(hits), max(hits)


def demo_damage() -> None:
    """Print aggregate statistics for a sample hit list."""
    hits = [10, 45, 90, 12, 70, 83]
    total, average, maximum = analyze_damage(hits)
    print(f"Total: {total}, Average: {average:.1f}, Maximum: {maximum}")


def demo_unique_visitors() -> None:
    """Demonstrate set uniqueness, intersection, and difference."""
    visitors = {101, 202, 303, 404}
    premium_users = {202, 555, 777}

    print("All visitors:", visitors)
    print("Number of unique visitors:", len(visitors))
    print("Premium visitors:", visitors & premium_users)
    print("Non-premium visitors:", visitors - premium_users)


def get_products_with_tag(
    products: list[dict[str, Any]], tag: str
) -> list[dict[str, Any]]:
    """Return every product whose tag set contains *tag*."""
    return [product for product in products if tag in product["tags"]]


def demo_products() -> None:
    """Filter a sample product catalog by tag."""
    products = [
        {"name": "Tea", "price": 12.5, "tags": {"drink", "hot"}},
        {"name": "Apple", "price": 3.0, "tags": {"fruit", "food"}},
        {"name": "Coffee", "price": 15.0, "tags": {"drink", "hot"}},
    ]
    tag = "drink"

    print(f'Products with the "{tag}" tag:')
    for product in get_products_with_tag(products, tag):
        print(f"- {product['name']} (price: {product['price']})")


def demo_log_parsing() -> None:
    """Parse selected key-value fields from a sample application log line."""
    log_line = (
        "2025-11-16 17:42:10 WARNING User:moshe-m-ofer "
        "Action:PasswordAttempt Status:Failed Attempts:3 "
        "IP:192.168.1.77 Location:IL-TLV"
    )

    fields: list[tuple[str, str]] = []
    for field in log_line.split()[2:]:
        if ":" not in field:
            continue
        key, value = field.split(":", 1)
        if key == "User":
            value = value.replace("-", " ")
        fields.append((key, value))

    print("\nClean summary:")
    for key, value in fields:
        print(f"{key} = {value}")


if __name__ == "__main__":
    demo_log_parsing()
    demo_damage()
    demo_unique_visitors()
    demo_products()
