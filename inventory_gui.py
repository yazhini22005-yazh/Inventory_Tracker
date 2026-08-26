import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = "inventory.json"

inventory = {}
sales_history = []
bill_number = 1001


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F4F7FB"
SIDEBAR_COLOR = "#172554"
SIDEBAR_HOVER = "#1E3A8A"

PRIMARY_COLOR = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"

TEXT_COLOR = "#1F2937"
MUTED_TEXT = "#6B7280"

WHITE = "#FFFFFF"

CARD_COLOR = "#FFFFFF"
BORDER_COLOR = "#E5E7EB"

SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"


# =========================================================
# LOAD DATA
# =========================================================

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
        messagebox.showwarning(
            "Warning",
            "Could not load existing inventory data."
        )

        inventory = {}
        sales_history = []
        bill_number = 1001


# =========================================================
# SAVE DATA
# =========================================================

def save_data():
    data = {
        "inventory": inventory,
        "sales_history": sales_history,
        "bill_number": bill_number
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError:
        messagebox.showerror(
            "Error",
            "Could not save data."
        )
        return False


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title("Inventory Tracker")

window.geometry("1250x750")

window.minsize(1100, 680)

window.configure(bg=BG_COLOR)


# =========================================================
# TKINTER STYLE
# =========================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass


# =========================================================
# TTK STYLES
# =========================================================

style.configure(
    "Title.TLabel",
    font=("Segoe UI", 24, "bold"),
    foreground=TEXT_COLOR,
    background=BG_COLOR
)

style.configure(
    "Heading.TLabel",
    font=("Segoe UI", 18, "bold"),
    foreground=TEXT_COLOR,
    background=BG_COLOR
)

style.configure(
    "Normal.TLabel",
    font=("Segoe UI", 10),
    foreground=TEXT_COLOR,
    background=BG_COLOR
)

style.configure(
    "Muted.TLabel",
    font=("Segoe UI", 10),
    foreground=MUTED_TEXT,
    background=BG_COLOR
)

style.configure(
    "Card.TLabel",
    font=("Segoe UI", 12, "bold"),
    foreground=TEXT_COLOR,
    background=CARD_COLOR
)

style.configure(
    "CardNumber.TLabel",
    font=("Segoe UI", 20, "bold"),
    foreground=TEXT_COLOR,
    background=CARD_COLOR
)

style.configure(
    "Main.TButton",
    font=("Segoe UI", 10, "bold"),
    foreground=WHITE,
    background=PRIMARY_COLOR,
    padding=(16, 10),
    borderwidth=0
)

style.map(
    "Main.TButton",
    background=[
        ("active", PRIMARY_HOVER),
        ("pressed", PRIMARY_HOVER)
    ]
)

style.configure(
    "TEntry",
    font=("Segoe UI", 10),
    padding=8
)

style.configure(
    "TCombobox",
    font=("Segoe UI", 10),
    padding=7
)

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT_COLOR,
    fieldbackground=WHITE,
    rowheight=34,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E8EEF7",
    foreground=TEXT_COLOR,
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", TEXT_COLOR)
    ]
)


# =========================================================
# GLOBAL LABEL REFERENCES
# =========================================================

products_number_label = None
stock_number_label = None
low_number_label = None
out_number_label = None
sales_number_label = None
profit_number_label = None


# =========================================================
# CLEAR CONTENT
# =========================================================

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# =========================================================
# UPDATE DASHBOARD VALUES
# =========================================================

def update_dashboard_values():

    total_products = len(inventory)

    total_stock = sum(
        product.get("quantity", 0)
        for product in inventory.values()
    )

    low_stock = sum(
        1
        for product in inventory.values()
        if 0 < product.get("quantity", 0)
        <= product.get("minimum_stock", 0)
    )

    out_of_stock = sum(
        1
        for product in inventory.values()
        if product.get("quantity", 0) == 0
    )

    total_sales = sum(
        sale.get("total_amount", 0)
        for sale in sales_history
    )

    total_profit = sum(
        sale.get("total_profit", 0)
        for sale in sales_history
    )

    if products_number_label is not None:
        products_number_label.config(
            text=str(total_products)
        )

    if stock_number_label is not None:
        stock_number_label.config(
            text=str(total_stock)
        )

    if low_number_label is not None:
        low_number_label.config(
            text=str(low_stock)
        )

    if out_number_label is not None:
        out_number_label.config(
            text=str(out_of_stock)
        )

    if sales_number_label is not None:
        sales_number_label.config(
            text=f"₹{total_sales:,.2f}"
        )

    if profit_number_label is not None:
        profit_number_label.config(
            text=f"₹{total_profit:,.2f}"
        )


# =========================================================
# CARD CREATOR
# =========================================================

def create_dashboard_card(parent, title, value, icon, accent_color):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
        bd=0
    )

    card.pack_propagate(False)

    left_line = tk.Frame(
        card,
        bg=accent_color,
        width=5
    )

    left_line.pack(
        side="left",
        fill="y"
    )

    content = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    content.pack(
        side="left",
        fill="both",
        expand=True,
        padx=15,
        pady=12
    )

    icon_label = tk.Label(
        content,
        text=icon,
        font=("Segoe UI Emoji", 20),
        bg=CARD_COLOR,
        fg=accent_color
    )

    icon_label.pack(
        anchor="w"
    )

    title_label = tk.Label(
        content,
        text=title,
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=MUTED_TEXT
    )

    title_label.pack(
        anchor="w"
    )

    value_label = tk.Label(
        content,
        text=value,
        font=("Segoe UI", 20, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    value_label.pack(
        anchor="w",
        pady=(3, 0)
    )

    return card, value_label


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    global products_number_label
    global stock_number_label
    global low_number_label
    global out_number_label
    global sales_number_label
    global profit_number_label

    clear_content()

    header = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    title = tk.Label(
        header,
        text="Dashboard",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )

    title.pack(
        anchor="w"
    )

    subtitle = tk.Label(
        header,
        text="Overview of your inventory and sales",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    )

    subtitle.pack(
        anchor="w",
        pady=(4, 0)
    )

    cards_frame = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    cards_frame.pack(
        fill="x",
        padx=30,
        pady=15
    )

    for column in range(3):
        cards_frame.columnconfigure(
            column,
            weight=1
        )

    card1, products_number_label = create_dashboard_card(
        cards_frame,
        "Total Products",
        "0",
        "📦",
        PRIMARY_COLOR
    )

    card1.grid(
        row=0,
        column=0,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    card2, stock_number_label = create_dashboard_card(
        cards_frame,
        "Total Stock",
        "0",
        "📊",
        "#0891B2"
    )

    card2.grid(
        row=0,
        column=1,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    card3, low_number_label = create_dashboard_card(
        cards_frame,
        "Low Stock",
        "0",
        "⚠️",
        WARNING_COLOR
    )

    card3.grid(
        row=0,
        column=2,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    card4, out_number_label = create_dashboard_card(
        cards_frame,
        "Out of Stock",
        "0",
        "❌",
        DANGER_COLOR
    )

    card4.grid(
        row=1,
        column=0,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    card5, sales_number_label = create_dashboard_card(
        cards_frame,
        "Total Sales",
        "₹0.00",
        "💰",
        SUCCESS_COLOR
    )

    card5.grid(
        row=1,
        column=1,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    card6, profit_number_label = create_dashboard_card(
        cards_frame,
        "Total Profit",
        "₹0.00",
        "📈",
        "#7C3AED"
    )

    card6.grid(
        row=1,
        column=2,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    # Recent products section
    section = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    section.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=15
    )

    section_title = tk.Label(
        section,
        text="Recent Inventory",
        font=("Segoe UI", 15, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    section_title.pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    recent_frame = tk.Frame(
        section,
        bg=CARD_COLOR
    )

    recent_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    columns = (
        "id",
        "name",
        "category",
        "stock",
        "price",
        "status"
    )

    tree = ttk.Treeview(
        recent_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "id": "Product ID",
        "name": "Product",
        "category": "Category",
        "stock": "Stock",
        "price": "Selling Price",
        "status": "Status"
    }

    widths = {
        "id": 100,
        "name": 160,
        "category": 140,
        "stock": 100,
        "price": 120,
        "status": 130
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=widths[column],
            anchor="center"
        )

    tree.pack(
        fill="both",
        expand=True
    )

    items = list(inventory.items())[-8:]

    for product_id, product in reversed(items):

        stock = product.get("quantity", 0)

        if stock == 0:
            status = "OUT OF STOCK"

        elif stock <= product.get("minimum_stock", 0):
            status = "LOW STOCK"

        else:
            status = "OK"

        tree.insert(
            "",
            "end",
            values=(
                product_id,
                product.get("name", ""),
                product.get("category", ""),
                stock,
                f"₹{product.get('selling_price', 0):.2f}",
                status
            )
        )

    update_dashboard_values()


# =========================================================
# ADD PRODUCT
# =========================================================

def show_add_product():

    clear_content()

    header = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    tk.Label(
        header,
        text="Add Product",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Add a new product to your inventory",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(anchor="w", pady=(4, 0))

    form_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    form_card.pack(
        padx=30,
        pady=20,
        fill="x"
    )

    form = tk.Frame(
        form_card,
        bg=CARD_COLOR
    )

    form.pack(
        padx=35,
        pady=30
    )

    variables = {
        "Product ID": tk.StringVar(),
        "Product Name": tk.StringVar(),
        "Category": tk.StringVar(),
        "Purchase Price": tk.StringVar(),
        "Selling Price": tk.StringVar(),
        "Initial Stock": tk.StringVar(),
        "Minimum Stock": tk.StringVar()
    }

    entries = {}

    row = 0

    for label_text, variable in variables.items():

        tk.Label(
            form,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).grid(
            row=row,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        entry = ttk.Entry(
            form,
            textvariable=variable,
            width=40
        )

        entry.grid(
            row=row,
            column=1,
            padx=15,
            pady=10
        )

        entries[label_text] = entry

        row += 1

    def save_product():

        product_id = variables["Product ID"].get().strip()
        name = variables["Product Name"].get().strip()
        category = variables["Category"].get().strip()

        if not product_id or not name or not category:

            messagebox.showwarning(
                "Warning",
                "Please fill Product ID, Name and Category."
            )

            return

        if product_id in inventory:

            messagebox.showerror(
                "Error",
                "Product ID already exists."
            )

            return

        try:

            purchase_price = float(
                variables["Purchase Price"].get()
            )

            selling_price = float(
                variables["Selling Price"].get()
            )

            quantity = int(
                variables["Initial Stock"].get()
            )

            minimum_stock = int(
                variables["Minimum Stock"].get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid numbers."
            )

            return

        if (
            purchase_price < 0
            or selling_price < 0
            or quantity < 0
            or minimum_stock < 0
        ):

            messagebox.showerror(
                "Error",
                "Values cannot be negative."
            )

            return

        if selling_price < purchase_price:

            continue_anyway = messagebox.askyesno(
                "Price Warning",
                "Selling price is lower than purchase price.\n\n"
                "Do you want to continue?"
            )

            if not continue_anyway:
                return

        inventory[product_id] = {
            "name": name,
            "category": category,
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "quantity": quantity,
            "minimum_stock": minimum_stock
        }

        if save_data():

            messagebox.showinfo(
                "Success",
                f"{name} added successfully!"
            )

            for variable in variables.values():
                variable.set("")

            update_dashboard_values()

    button_frame = tk.Frame(
        form_card,
        bg=CARD_COLOR
    )

    button_frame.pack(
        pady=(0, 30)
    )

    ttk.Button(
        button_frame,
        text="ADD PRODUCT",
        style="Main.TButton",
        command=save_product
    ).pack()

    entries["Product ID"].focus()


# =========================================================
# VIEW PRODUCTS
# =========================================================

def show_products():

    clear_content()

    header = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    tk.Label(
        header,
        text="Product Inventory",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        header,
        text="View and search all products",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(anchor="w", pady=(4, 0))

    search_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    search_card.pack(
        fill="x",
        padx=30,
        pady=15
    )

    search_inner = tk.Frame(
        search_card,
        bg=CARD_COLOR
    )

    search_inner.pack(
        padx=20,
        pady=15
    )

    tk.Label(
        search_inner,
        text="Search Product:",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left", padx=(0, 10))

    search_var = tk.StringVar()

    ttk.Entry(
        search_inner,
        textvariable=search_var,
        width=40
    ).pack(side="left")

    table_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    table_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    columns = (
        "id",
        "name",
        "category",
        "purchase",
        "selling",
        "stock",
        "minimum",
        "status"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "id": "Product ID",
        "name": "Name",
        "category": "Category",
        "purchase": "Purchase",
        "selling": "Selling",
        "stock": "Stock",
        "minimum": "Min Stock",
        "status": "Status"
    }

    widths = {
        "id": 100,
        "name": 150,
        "category": 130,
        "purchase": 100,
        "selling": 100,
        "stock": 90,
        "minimum": 90,
        "status": 130
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=widths[column],
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def populate_table(*args):

        for row in tree.get_children():
            tree.delete(row)

        search_text = search_var.get().lower().strip()

        for product_id, product in inventory.items():

            searchable = (
                f"{product_id} "
                f"{product.get('name', '')} "
                f"{product.get('category', '')}"
            ).lower()

            if search_text and search_text not in searchable:
                continue

            stock = product.get("quantity", 0)
            minimum = product.get("minimum_stock", 0)

            if stock == 0:
                status = "OUT OF STOCK"

            elif stock <= minimum:
                status = "LOW STOCK"

            else:
                status = "OK"

            tree.insert(
                "",
                "end",
                values=(
                    product_id,
                    product.get("name", ""),
                    product.get("category", ""),
                    f"₹{product.get('purchase_price', 0):.2f}",
                    f"₹{product.get('selling_price', 0):.2f}",
                    stock,
                    minimum,
                    status
                )
            )

    search_var.trace_add(
        "write",
        populate_table
    )

    populate_table()


# =========================================================
# CREATE BILL
# =========================================================

def show_billing():

    clear_content()

    header = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    tk.Label(
        header,
        text="Create Bill",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Create a bill with multiple products",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(anchor="w", pady=(4, 0))

    top_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    top_card.pack(
        fill="x",
        padx=30,
        pady=15
    )

    top_inner = tk.Frame(
        top_card,
        bg=CARD_COLOR
    )

    top_inner.pack(
        padx=20,
        pady=15
    )

    tk.Label(
        top_inner,
        text="Customer Name",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    customer_var = tk.StringVar()

    ttk.Entry(
        top_inner,
        textvariable=customer_var,
        width=30
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Label(
        top_inner,
        text="Product",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    product_var = tk.StringVar()

    product_combo = ttk.Combobox(
        top_inner,
        textvariable=product_var,
        width=28,
        state="readonly"
    )

    product_combo.grid(
        row=0,
        column=3,
        padx=10
    )

    tk.Label(
        top_inner,
        text="Quantity",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=4,
        padx=10
    )

    quantity_var = tk.StringVar(value="1")

    ttk.Entry(
        top_inner,
        textvariable=quantity_var,
        width=10
    ).grid(
        row=0,
        column=5,
        padx=10
    )

    cart = []

    def update_products():

        product_list = []

        for product_id, product in inventory.items():

            if product.get("quantity", 0) > 0:

                product_list.append(
                    f"{product_id} - {product.get('name', '')}"
                )

        product_combo["values"] = product_list

        if product_list:

            product_combo.current(0)

    def refresh_cart():

        for row in cart_tree.get_children():
            cart_tree.delete(row)

        total_amount = 0

        for item in cart:

            cart_tree.insert(
                "",
                "end",
                values=(
                    item["product_id"],
                    item["product_name"],
                    item["quantity"],
                    f"₹{item['price']:.2f}",
                    f"₹{item['total']:.2f}"
                )
            )

            total_amount += item["total"]

        total_label.config(
            text=f"Total Amount: ₹{total_amount:,.2f}"
        )

    def add_to_cart():

        selected = product_var.get().strip()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a product."
            )

            return

        product_id = selected.split(" - ")[0]

        if product_id not in inventory:

            messagebox.showerror(
                "Error",
                "Product not found."
            )

            return

        try:

            quantity = int(
                quantity_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0."
            )

            return

        product = inventory[product_id]

        already_added = 0

        for item in cart:

            if item["product_id"] == product_id:

                already_added += item["quantity"]

        available = product["quantity"] - already_added

        if quantity > available:

            messagebox.showerror(
                "Stock Error",
                f"Only {available} available."
            )

            return

        existing = None

        for item in cart:

            if item["product_id"] == product_id:

                existing = item
                break

        if existing:

            existing["quantity"] += quantity

            existing["total"] = (
                existing["quantity"]
                * existing["price"]
            )

            existing["profit"] = (
                existing["quantity"]
                * (
                    existing["price"]
                    - existing["purchase_price"]
                )
            )

        else:

            total = (
                quantity
                * product["selling_price"]
            )

            profit = (
                quantity
                * (
                    product["selling_price"]
                    - product["purchase_price"]
                )
            )

            cart.append(
                {
                    "product_id": product_id,
                    "product_name": product["name"],
                    "quantity": quantity,
                    "price": product["selling_price"],
                    "purchase_price": product["purchase_price"],
                    "total": total,
                    "profit": profit
                }
            )

        quantity_var.set("1")

        refresh_cart()

    def remove_cart_item():

        selected = cart_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select an item from the bill."
            )

            return

        values = cart_tree.item(
            selected[0],
            "values"
        )

        product_id = values[0]

        for index, item in enumerate(cart):

            if item["product_id"] == product_id:

                cart.pop(index)
                break

        refresh_cart()

    def complete_bill():

        global bill_number

        if not cart:

            messagebox.showwarning(
                "Warning",
                "Please add products to the bill."
            )

            return

        customer = customer_var.get().strip()

        if not customer:

            customer = "Walk-in Customer"

        total_items = sum(
            item["quantity"]
            for item in cart
        )

        total_amount = sum(
            item["total"]
            for item in cart
        )

        total_profit = sum(
            item["profit"]
            for item in cart
        )

        date_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        # Update stock
        for item in cart:

            product_id = item["product_id"]

            inventory[product_id]["quantity"] -= (
                item["quantity"]
            )

        sale = {
            "bill_number": bill_number,
            "customer_name": customer,
            "date_time": date_time,
            "items": cart.copy(),
            "total_items": total_items,
            "total_amount": total_amount,
            "total_profit": total_profit
        }

        sales_history.append(sale)

        if not save_data():
            return

        bill_text = ""

        bill_text += (
            "================================\n"
            f"          BILL #{bill_number}\n"
            "================================\n"
        )

        bill_text += f"Customer: {customer}\n"
        bill_text += f"Date: {date_time}\n"
        bill_text += "--------------------------------\n"

        for item in cart:

            bill_text += (
                f"{item['product_name']}\n"
                f"{item['quantity']} x "
                f"₹{item['price']:.2f} = "
                f"₹{item['total']:.2f}\n"
            )

        bill_text += "--------------------------------\n"
        bill_text += (
            f"Total Items: {total_items}\n"
            f"Total Amount: ₹{total_amount:,.2f}\n"
            f"Total Profit: ₹{total_profit:,.2f}\n"
        )

        bill_text += "================================"

        messagebox.showinfo(
            f"Bill #{bill_number}",
            bill_text
        )

        warnings = []

        for item in cart:

            product = inventory[item["product_id"]]

            stock = product["quantity"]

            if stock == 0:

                warnings.append(
                    f"❌ {product['name']} "
                    f"→ OUT OF STOCK"
                )

            elif stock <= product["minimum_stock"]:

                warnings.append(
                    f"⚠️ {product['name']} "
                    f"→ LOW STOCK ({stock})"
                )

        bill_number += 1

        save_data()

        if warnings:

            messagebox.showwarning(
                "Stock Alert",
                "\n".join(warnings)
            )

        update_dashboard_values()

        show_billing()

    action_frame = tk.Frame(
        top_card,
        bg=CARD_COLOR
    )

    action_frame.pack(
        pady=(0, 15)
    )

    ttk.Button(
        action_frame,
        text="ADD TO BILL",
        style="Main.TButton",
        command=add_to_cart
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        action_frame,
        text="REMOVE SELECTED",
        command=remove_cart_item
    ).pack(
        side="left",
        padx=5
    )

    # Cart section
    cart_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    cart_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    tk.Label(
        cart_card,
        text="Current Bill",
        font=("Segoe UI", 15, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    cart_frame = tk.Frame(
        cart_card,
        bg=CARD_COLOR
    )

    cart_frame.pack(
        fill="both",
        expand=True,
        padx=20
    )

    cart_columns = (
        "id",
        "name",
        "quantity",
        "price",
        "total"
    )

    cart_tree = ttk.Treeview(
        cart_frame,
        columns=cart_columns,
        show="headings"
    )

    cart_headings = {
        "id": "Product ID",
        "name": "Product",
        "quantity": "Quantity",
        "price": "Price",
        "total": "Total"
    }

    for column in cart_columns:

        cart_tree.heading(
            column,
            text=cart_headings[column]
        )

        cart_tree.column(
            column,
            width=160,
            anchor="center"
        )

    cart_tree.pack(
        fill="both",
        expand=True
    )

    total_label = tk.Label(
        cart_card,
        text="Total Amount: ₹0.00",
        font=("Segoe UI", 18, "bold"),
        bg=CARD_COLOR,
        fg=PRIMARY_COLOR
    )

    total_label.pack(
        anchor="e",
        padx=30,
        pady=15
    )

    ttk.Button(
        cart_card,
        text="COMPLETE BILL",
        style="Main.TButton",
        command=complete_bill
    ).pack(
        pady=(0, 20)
    )

    update_products()


# =========================================================
# RESTOCK
# =========================================================

def show_restock():

    clear_content()

    tk.Label(
        content_frame,
        text="Restock Product",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        content_frame,
        text="Increase stock for an existing product",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(
        anchor="w",
        padx=30
    )

    card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.pack(
        padx=30,
        pady=25,
        fill="x"
    )

    form = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    form.pack(
        pady=30
    )

    tk.Label(
        form,
        text="Select Product",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=0,
        padx=15,
        pady=12
    )

    product_var = tk.StringVar()

    product_combo = ttk.Combobox(
        form,
        textvariable=product_var,
        width=35,
        state="readonly"
    )

    product_combo.grid(
        row=0,
        column=1,
        padx=15,
        pady=12
    )

    tk.Label(
        form,
        text="Quantity to Add",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=1,
        column=0,
        padx=15,
        pady=12
    )

    quantity_var = tk.StringVar()

    ttk.Entry(
        form,
        textvariable=quantity_var,
        width=38
    ).grid(
        row=1,
        column=1,
        padx=15,
        pady=12
    )

    def populate_products():

        values = []

        for product_id, product in inventory.items():

            values.append(
                f"{product_id} - {product.get('name', '')}"
            )

        product_combo["values"] = values

        if values:
            product_combo.current(0)

    def restock():

        selected = product_var.get().strip()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a product."
            )

            return

        product_id = selected.split(" - ")[0]

        try:

            quantity = int(
                quantity_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0."
            )

            return

        inventory[product_id]["quantity"] += quantity

        if save_data():

            messagebox.showinfo(
                "Success",
                f"Stock updated successfully!\n\n"
                f"New Stock: "
                f"{inventory[product_id]['quantity']}"
            )

            quantity_var.set("")

            update_dashboard_values()

    ttk.Button(
        card,
        text="RESTOCK PRODUCT",
        style="Main.TButton",
        command=restock
    ).pack(
        pady=(0, 30)
    )

    populate_products()


# =========================================================
# SALES REPORT
# =========================================================

def show_sales_report():

    clear_content()

    tk.Label(
        content_frame,
        text="Sales Report",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        content_frame,
        text="View sales, bills and profit",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(
        anchor="w",
        padx=30
    )

    total_bills = len(sales_history)

    total_items = sum(
        sale.get("total_items", 0)
        for sale in sales_history
    )

    total_sales = sum(
        sale.get("total_amount", 0)
        for sale in sales_history
    )

    total_profit = sum(
        sale.get("total_profit", 0)
        for sale in sales_history
    )

    summary = tk.Frame(
        content_frame,
        bg=BG_COLOR
    )

    summary.pack(
        fill="x",
        padx=30,
        pady=20
    )

    summary.columnconfigure(
        0,
        weight=1
    )

    summary.columnconfigure(
        1,
        weight=1
    )

    summary.columnconfigure(
        2,
        weight=1
    )

    summary.columnconfigure(
        3,
        weight=1
    )

    summary_values = [
        ("Bills", str(total_bills), PRIMARY_COLOR),
        ("Items Sold", str(total_items), "#0891B2"),
        ("Sales", f"₹{total_sales:,.2f}", SUCCESS_COLOR),
        ("Profit", f"₹{total_profit:,.2f}", "#7C3AED")
    ]

    for index, (label_text, value_text, color) in enumerate(summary_values):

        card = tk.Frame(
            summary,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=index,
            padx=6,
            sticky="nsew"
        )

        tk.Label(
            card,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=MUTED_TEXT
        ).pack(
            pady=(15, 4)
        )

        tk.Label(
            card,
            text=value_text,
            font=("Segoe UI", 18, "bold"),
            bg=CARD_COLOR,
            fg=color
        ).pack(
            pady=(0, 15)
        )

    table_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    table_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    columns = (
        "bill",
        "customer",
        "date",
        "items",
        "amount",
        "profit"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "bill": "Bill No",
        "customer": "Customer",
        "date": "Date & Time",
        "items": "Items",
        "amount": "Amount",
        "profit": "Profit"
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=160,
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for sale in sales_history:

        tree.insert(
            "",
            "end",
            values=(
                sale.get("bill_number", ""),
                sale.get("customer_name", ""),
                sale.get("date_time", ""),
                sale.get("total_items", 0),
                f"₹{sale.get('total_amount', 0):,.2f}",
                f"₹{sale.get('total_profit', 0):,.2f}"
            )
        )


# =========================================================
# STOCK ALERTS
# =========================================================

def show_stock_alerts():

    clear_content()

    tk.Label(
        content_frame,
        text="Stock Alerts",
        font=("Segoe UI", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        content_frame,
        text="Products that need attention",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=MUTED_TEXT
    ).pack(
        anchor="w",
        padx=30
    )

    table_card = tk.Frame(
        content_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    table_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    columns = (
        "id",
        "name",
        "stock",
        "minimum",
        "status"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "id": "Product ID",
        "name": "Product",
        "stock": "Current Stock",
        "minimum": "Minimum Stock",
        "status": "Status"
    }

    for column in columns:

        tree.heading(
            column,
            text=headings[column]
        )

        tree.column(
            column,
            width=180,
            anchor="center"
        )

    tree.pack(
        fill="both",
        expand=True
    )

    found = False

    for product_id, product in inventory.items():

        stock = product.get("quantity", 0)
        minimum = product.get("minimum_stock", 0)

        if stock == 0:

            status = "OUT OF STOCK"

            found = True

        elif stock <= minimum:

            status = "LOW STOCK"

            found = True

        else:

            continue

        tree.insert(
            "",
            "end",
            values=(
                product_id,
                product.get("name", ""),
                stock,
                minimum,
                status
            )
        )

    if not found:

        tk.Label(
            table_card,
            text="✅ All products have sufficient stock.",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=SUCCESS_COLOR
        ).pack(
            pady=15
        )


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    window,
    width=235,
    bg=SIDEBAR_COLOR
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# Sidebar title
sidebar_title = tk.Label(
    sidebar,
    text="INVENTORY\nTRACKER",
    font=("Segoe UI", 20, "bold"),
    fg=WHITE,
    bg=SIDEBAR_COLOR,
    justify="center"
)

sidebar_title.pack(
    pady=(30, 25)
)


# Subtitle
sidebar_subtitle = tk.Label(
    sidebar,
    text="Smart Stock Management",
    font=("Segoe UI", 9),
    fg="#BFDBFE",
    bg=SIDEBAR_COLOR
)

sidebar_subtitle.pack(
    pady=(0, 20)
)


# =========================================================
# SIDEBAR BUTTON
# =========================================================

def sidebar_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        font=("Segoe UI", 10, "bold"),
        fg=WHITE,
        bg=SIDEBAR_COLOR,
        activeforeground=WHITE,
        activebackground=SIDEBAR_HOVER,
        relief="flat",
        bd=0,
        width=23,
        command=command,
        pady=11,
        cursor="hand2",
        anchor="w",
        padx=20
    )

    button.pack(
        pady=3,
        padx=10,
        fill="x"
    )

    return button


sidebar_button(
    "🏠   Dashboard",
    show_dashboard
)

sidebar_button(
    "➕   Add Product",
    show_add_product
)

sidebar_button(
    "📦   View Products",
    show_products
)

sidebar_button(
    "🧾   Create Bill",
    show_billing
)

sidebar_button(
    "📥   Restock",
    show_restock
)

sidebar_button(
    "📊   Sales Report",
    show_sales_report
)

sidebar_button(
    "⚠️   Stock Alerts",
    show_stock_alerts
)


# =========================================================
# EXIT BUTTON
# =========================================================

exit_button = tk.Button(
    sidebar,
    text="✕   Exit",
    font=("Segoe UI", 10, "bold"),
    fg=WHITE,
    bg="#B91C1C",
    activeforeground=WHITE,
    activebackground="#991B1B",
    relief="flat",
    bd=0,
    width=23,
    pady=11,
    cursor="hand2",
    command=window.destroy
)

exit_button.pack(
    side="bottom",
    pady=20,
    padx=10,
    fill="x"
)


# =========================================================
# CONTENT FRAME
# =========================================================

content_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================================================
# LOAD DATA
# =========================================================

load_data()


# =========================================================
# SHOW DASHBOARD
# =========================================================

show_dashboard()


# =========================================================
# START APP
# =========================================================

window.mainloop()