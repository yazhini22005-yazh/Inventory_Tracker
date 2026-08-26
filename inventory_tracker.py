import json
import os
from datetime import datetime

DATA_FILE = "inventory.json"
inventory = {}
sales_history = []
bill_number = 1001

# LOAD DATA
def load_data():
    global inventory, sales_history, bill_number

    if not os.path.exists(DATA_FILE):
        inventory = {}
        sales_history = []
        bill_number = 1001
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        inventory = data.get("inventory", {})
        sales_history = data.get("sales_history", [])
        bill_number = data.get("bill_number", 1001)

    except (json.JSONDecodeError, OSError):
        print("⚠️ Could not load existing data.")
        inventory = {}
        sales_history = []
        bill_number = 1001
# SAVE DATA
def save_data():
    data = {
        "inventory": inventory,
        "sales_history": sales_history,
        "bill_number": bill_number
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError:
        print("❌ Could not save data.")
#  ADD PRODUCT
def add_product():
    print("\n===== ADD PRODUCT =====")

    product_id = input("Enter Product ID: ").strip()

    if not product_id:
        print("❌ Product ID cannot be empty.")
        return

    if product_id in inventory:
        print("❌ Product ID already exists!")
        return

    name = input("Enter Product Name: ").strip()
    category = input("Enter Category: ").strip()

    if not name or not category:
        print("❌ Product name and category cannot be empty.")
        return

    try:
        purchase_price = float(input("Enter Purchase Price: ₹"))
        selling_price = float(input("Enter Selling Price: ₹"))
        quantity = int(input("Enter Initial Stock Quantity: "))
        minimum_stock = int(input("Enter Minimum Stock Level: "))

        if purchase_price < 0 or selling_price < 0:
            print("❌ Price cannot be negative.")
            return

        if quantity < 0 or minimum_stock < 0:
            print("❌ Quantity cannot be negative.")
            return

        if selling_price < purchase_price:
            print("⚠️ WARNING: Selling price is lower than purchase price.")

    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    inventory[product_id] = {
        "name": name,
        "category": category,
        "purchase_price": purchase_price,
        "selling_price": selling_price,
        "quantity": quantity,
        "minimum_stock": minimum_stock
    }

    save_data()

    print("\n✅ Product added successfully!")
#  VIEW PRODUCTS
def view_products():
    print("\n===== CURRENT INVENTORY =====")

    if not inventory:
        print("❌ No products available.")
        return

    for product_id, product in inventory.items():

        print("\n------------------------------------------")
        print(f"Product ID      : {product_id}")
        print(f"Product Name    : {product['name']}")
        print(f"Category        : {product['category']}")
        print(f"Purchase Price  : ₹{product['purchase_price']:.2f}")
        print(f"Selling Price   : ₹{product['selling_price']:.2f}")
        print(f"Current Stock   : {product['quantity']}")
        print(f"Minimum Stock   : {product['minimum_stock']}")

        if product["quantity"] == 0:
            print("❌ OUT OF STOCK!")

        elif product["quantity"] <= product["minimum_stock"]:
            print("⚠️ LOW STOCK ALERT!")
# SELL MULTIPLE PRODUCTS
def create_bill():
    global bill_number

    print("\n===== CREATE BILL =====")

    if not inventory:
        print("❌ No products available.")
        return

    customer_name = input("Enter Customer Name: ").strip()

    if not customer_name:
        customer_name = "Walk-in Customer"

    cart = []

    while True:

        print("\n------------------------------------------")
        print("Available Products:")

        for product_id, product in inventory.items():
            print(
                f"{product_id} - {product['name']} "
                f"(Stock: {product['quantity']})"
            )

        print("------------------------------------------")

        product_id = input(
            "Enter Product ID (or 'done' to finish): "
        ).strip()

        if product_id.lower() == "done":
            break

        if product_id not in inventory:
            print("❌ Product not found!")
            continue

        product = inventory[product_id]

        if product["quantity"] <= 0:
            print("❌ This product is out of stock!")
            continue

        print(f"\nProduct: {product['name']}")
        print(f"Selling Price: ₹{product['selling_price']:.2f}")
        print(f"Available Stock: {product['quantity']}")

        try:
            quantity = int(input("Enter Quantity: "))

            if quantity <= 0:
                print("❌ Quantity must be greater than 0.")
                continue

        except ValueError:
            print("❌ Please enter a valid quantity.")
            continue

        # Check current cart quantity for same product
        already_added = 0

        for item in cart:
            if item["product_id"] == product_id:
                already_added += item["quantity"]

        available_after_cart = product["quantity"] - already_added

        if quantity > available_after_cart:
            print(
                f"❌ Not enough stock! "
                f"Only {available_after_cart} available."
            )
            continue

        item_total = quantity * product["selling_price"]

        item_profit = quantity * (
            product["selling_price"] - product["purchase_price"]
        )

        cart.append({
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "price": product["selling_price"],
            "total": item_total,
            "profit": item_profit
        })

        print("✅ Product added to bill.")

    # No products added
    if not cart:
        print("\n❌ No products added to bill.")
        return
    # CALCULATE BILL
    total_amount = 0
    total_profit = 0
    total_items = 0

    for item in cart:
        total_amount += item["total"]
        total_profit += item["profit"]
        total_items += item["quantity"]

    current_datetime = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    # UPDATE INVENTORY

    for item in cart:
        product_id = item["product_id"]
        inventory[product_id]["quantity"] -= item["quantity"]

    # SAVE SALE HISTORY
    sale = {
        "bill_number": bill_number,
        "customer_name": customer_name,
        "date_time": current_datetime,
        "items": cart,
        "total_items": total_items,
        "total_amount": total_amount,
        "total_profit": total_profit
    }

    sales_history.append(sale)

    save_data()
    # DISPLAY BILL
    print("\n")
    print("==========================================")
    print(f"              BILL #{bill_number}")
    print("==========================================")
    print(f"Customer : {customer_name}")
    print(f"Date     : {current_datetime}")
    print("------------------------------------------")

    for item in cart:
        print(
            f"{item['product_name']:<15} "
            f"{item['quantity']} x "
            f"₹{item['price']:.2f} = "
            f"₹{item['total']:.2f}"
        )

    print("------------------------------------------")
    print(f"Total Items  : {total_items}")
    print(f"Total Amount : ₹{total_amount:.2f}")
    print(f"Total Profit : ₹{total_profit:.2f}")
    print("==========================================")

    print("\n✅ Bill created successfully!")
    # LOW STOCK ALERT
    print("\n===== STOCK STATUS =====")

    for item in cart:

        product_id = item["product_id"]
        product = inventory[product_id]

        if product["quantity"] == 0:
            print(
                f"❌ {product['name']} "
                f"→ OUT OF STOCK!"
            )

        elif product["quantity"] <= product["minimum_stock"]:
            print(
                f"⚠️ {product['name']} "
                f"→ LOW STOCK ({product['quantity']})"
            )

    bill_number += 1
    save_data()
# RESTOCK PRODUCT

def restock_product():
    print("\n===== RESTOCK PRODUCT =====")

    if not inventory:
        print("❌ No products available.")
        return

    product_id = input("Enter Product ID: ").strip()

    if product_id not in inventory:
        print("❌ Product not found!")
        return

    product = inventory[product_id]

    print(f"\nProduct Name  : {product['name']}")
    print(f"Current Stock : {product['quantity']}")

    try:
        quantity = int(input("Enter Quantity to Add: "))

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return

    except ValueError:
        print("❌ Please enter a valid quantity.")
        return

    product["quantity"] += quantity

    save_data()

    print("\n✅ Stock updated successfully!")
    print(f"New Stock : {product['quantity']}")

#  SALES REPORT
def sales_report():
    print("\n===== SALES REPORT =====")

    if not sales_history:
        print("❌ No sales recorded yet.")
        return

    total_bills = len(sales_history)
    total_items = 0
    total_sales = 0
    total_profit = 0

    for sale in sales_history:
        total_items += sale["total_items"]
        total_sales += sale["total_amount"]
        total_profit += sale["total_profit"]

    print("\n------------------------------------------")
    print(f"Total Bills       : {total_bills}")
    print(f"Total Items Sold  : {total_items}")
    print(f"Total Sales       : ₹{total_sales:.2f}")
    print(f"Total Profit      : ₹{total_profit:.2f}")
    print("------------------------------------------")

    print("\n===== BILL HISTORY =====")

    for sale in sales_history:

        print("\n------------------------------------------")
        print(f"Bill Number : {sale['bill_number']}")
        print(f"Customer    : {sale['customer_name']}")
        print(f"Date        : {sale['date_time']}")
        print("------------------------------------------")

        for item in sale["items"]:
            print(
                f"{item['product_name']} - "
                f"{item['quantity']} x "
                f"₹{item['price']:.2f} = "
                f"₹{item['total']:.2f}"
            )

        print(f"Total       : ₹{sale['total_amount']:.2f}")
        print(f"Profit      : ₹{sale['total_profit']:.2f}")
#  MAIN MENU
def main():

    load_data()

    while True:

        print("\n==========================================")
        print("           INVENTORY TRACKER")
        print("==========================================")

        print("1. Add Product")
        print("2. View Products")
        print("3. Create Bill / Sell Products")
        print("4. Restock Product")
        print("5. Sales Report")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            create_bill()

        elif choice == "4":
            restock_product()

        elif choice == "5":
            sales_report()

        elif choice == "6":
            save_data()
            print("\n✅ Data saved successfully.")
            print("Thank you for using Inventory Tracker! 👋")
            break

        else:
            print("\n❌ Invalid choice. Please select 1 to 6.")

if __name__ == "__main__":
    main()