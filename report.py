import os
from datetime import datetime

import pandas as pd

import database
from constants import SUCCESS


def generate_inventory_report():
    rows = database.get_inventory()

    if not rows:
        return None

    total_products = len(rows)

    total_units = sum(
        row[2] for row in rows
    )

    total_inventory_value = sum(
        row[2] * row[3] for row in rows
    )

    return {
        "total_products": total_products,
        "total_units": total_units,
        "total_inventory_value": total_inventory_value,
        "rows": rows
    }


def export_inventory_report():
    report_data = generate_inventory_report()

    if report_data is None:
        return None

    rows = report_data["rows"]

    total_products = report_data["total_products"]
    total_units = report_data["total_units"]
    total_inventory_value = report_data["total_inventory_value"]

    df = pd.DataFrame(
        rows,
        columns=["id", "product", "quantity", "price"]
    )

    df["product_value"] = df["price"] * df["quantity"]

    df = df.sort_values(
        by="product_value",
        ascending=False
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = f"inventory_report_{timestamp}.csv"

    os.makedirs("reports", exist_ok=True)

    filepath = os.path.join(
        "reports",
        filename
    )

    df.to_csv(filepath, index=False)

    return (
        SUCCESS,
        filepath,
        total_products,
        total_units,
        total_inventory_value
    )