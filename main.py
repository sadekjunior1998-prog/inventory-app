import database
import report

from constants import (
    SUCCESS,
    NOT_FOUND,
    ALREADY_EXISTS,
    INSUFFICIENT_STOCK,
)


def add_product():
    product = input("Enter product name: ").strip()

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    status = database.add_product(
        product,
        quantity,
        price
    )

    if status == SUCCESS:
        print("Product added successfully.")

    elif status == ALREADY_EXISTS:
        print("Product already exists.")

    else:
        print("An error occurred.")


def search_product():
    product = input("Enter product name: ").strip()

    result = database.search_product(product)

    if result is None:
        print("Product not found.")
    else:
        print(result)


def show_inventory():
    rows = database.get_inventory()

    if not rows:
        print("Inventory is empty.")
        return

    for row in rows:
        print(row)


def add_stock():
    product = input("Enter product name: ").strip()

    try:
        quantity = int(input("Enter quantity to add: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    status = database.add_stock(product, quantity)

    if status == SUCCESS:
        print("Stock added successfully.")

    elif status == NOT_FOUND:
        print("Product not found.")

    else:
        print("An error occurred.")


def remove_stock():
    product = input("Enter product name: ").strip()

    try:
        quantity = int(input("Enter quantity to remove: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    status = database.remove_stock(product, quantity)

    if status == SUCCESS:
        print("Stock removed successfully.")

    elif status == NOT_FOUND:
        print("Product not found.")

    elif status == INSUFFICIENT_STOCK:
        print("Insufficient stock.")

    else:
        print("An error occurred.")


def show_report():
    report_data = report.generate_inventory_report()

    if report_data is None:
        print("Inventory is empty.")
        return

    print(f"Total products: {report_data['total_products']}")
    print(f"Total units: {report_data['total_units']}")
    print(
        f"Total inventory value: "
        f"{report_data['total_inventory_value']:.2f}"
    )


def delete_product():
    product = input("Enter product name: ").strip()

    status = database.delete_product(product)

    if status == SUCCESS:
        print("Product deleted successfully.")

    elif status == NOT_FOUND:
        print("Product not found.")

    else:
        print("An error occurred.")


def export_report():
    result = report.export_inventory_report()

    if result is None:
        print("Inventory is empty.")
        return

    (
        status,
        filepath,
        total_products,
        total_units,
        total_inventory_value
    ) = result

    if status == SUCCESS:
        print(f"Report exported successfully: {filepath}")
        print(f"Products: {total_products}")
        print(f"Total units: {total_units}")
        print(
            f"Total inventory value: "
            f"{total_inventory_value:.2f}"
        )

    else:
        print("An error occurred while exporting the report.")


def main():
    database.initialize_database()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add product")
        print("2. Search product")
        print("3. Show inventory")
        print("4. Add stock")
        print("5. Remove stock")
        print("6. Show report")
        print("7. Delete product")
        print("8. Export report")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            search_product()

        elif choice == "3":
            show_inventory()

        elif choice == "4":
            add_stock()

        elif choice == "5":
            remove_stock()

        elif choice == "6":
            show_report()

        elif choice == "7":
            delete_product()

        elif choice == "8":
            export_report()

        elif choice == "9":
            break

        else:
            print("Invalid choice.")

    database.close_database()
    print("Goodbye!")


if __name__ == "__main__":
    main()