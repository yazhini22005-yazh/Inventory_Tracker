import streamlit as st
import json
import os
from datetime import datetime

# PAGE CONFIG

st.set_page_config(
    page_title="Inventory Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS

st.markdown("""
<style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f8fafc 100%
        );
    }


    /* ---------- MAIN CONTAINER ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ---------- FONT ---------- */

    html, body, [class*="css"] {
        font-family: "Segoe UI", Arial, sans-serif;
    }


    /* ---------- HEADINGS ---------- */

    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #1e293b 100%
        );
    }


    section[data-testid="stSidebar"] * {
        color: white !important;
    }


    /* ---------- SIDEBAR RADIO ---------- */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 8px;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 10px 12px;
        transition: 0.2s;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.14);
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        border: none;
        font-weight: 700;
        padding: 0.65rem 1rem;
        transition: all 0.2s ease;
    }


    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }


    /* ---------- FORM SUBMIT BUTTON ---------- */

    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 700;
    }


    /* ---------- INPUT BOXES ---------- */

    div[data-baseweb="input"] {
        border-radius: 9px;
    }


    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }


    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.90);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }


    div[data-testid="stMetricLabel"] {
        font-weight: 700;
    }


    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }


    /* ---------- DATAFRAME ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }


    /* ---------- ALERT BOXES ---------- */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ---------- CARDS ---------- */

    .custom-card {
        background: rgba(255,255,255,0.92);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 5px 20px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }


    .custom-card h3 {
        margin-top: 0;
    }


    /* ---------- BILL ---------- */

    .bill-card {
        background: white;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }


    .bill-total {
        font-size: 28px;
        font-weight: 800;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #64748b;
        padding: 25px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)

# FILES


INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"

# JSON LOAD
def load_json(filename):

    if not os.path.exists(filename):
        return {}

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {}

# JSON SAVE

def save_json(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )
# LOAD DATA

inventory = load_json(
    INVENTORY_FILE
)

sales = load_json(
    SALES_FILE
)


if not isinstance(sales, list):
    sales = []

# CALCULATIONS

total_products = len(inventory)

total_stock = sum(
    int(product.get("quantity", 0))
    for product in inventory.values()
)

low_stock_count = sum(
    1
    for product in inventory.values()
    if int(product.get("quantity", 0))
    <= int(product.get("minimum_stock", 0))
)

total_revenue = sum(
    float(sale.get("total", 0))
    for sale in sales
)

total_profit = sum(
    float(sale.get("profit", 0))
    for sale in sales
)

# HEADER


st.title("📦 Inventory Pro")

st.caption(
    "Smart Inventory & Sales Management System"
)

st.divider()
# SIDEBAR
st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 0 20px 0;
    ">
        <div style="font-size:45px;">📦</div>
        <h2 style="margin:0;">Inventory Pro</h2>
        <p style="color:#cbd5e1;">
            Management System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
menu = st.sidebar.radio(
    "NAVIGATION",
    [
        "⚙️ Dashboard",
        "➕ Add Product",
        "📋 View Products",
        "✏️ Update Product",
        "🗑️ Delete Product",
        "🛒 Customer Sale",
        "📊 Sales History",
        "🚨 Stock Alerts"
    ]
)
# DASHBOARD
if menu == "⚙️ Dashboard":

    st.header("⚙️ Dashboard")

    st.write(
        "Overview of your inventory and sales."
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📦 Products",
            total_products
        )


    with col2:

        st.metric(
            "📊 Current Stock",
            total_stock
        )


    with col3:

        st.metric(
            "💰 Revenue",
            f"₹{total_revenue:,.2f}"
        )


    with col4:

        st.metric(
            "📈 Profit",
            f"₹{total_profit:,.2f}"
        )


    st.write("")


    col5, col6 = st.columns(2)


    with col5:

        st.metric(
            "🧾 Total Bills",
            len(sales)
        )


    with col6:

        st.metric(
            "🚨 Low Stock Items",
            low_stock_count
        )


    st.divider()


    st.subheader("📦 Inventory Overview")


    if inventory:

        table_data = []


        for product_id, product in inventory.items():

            quantity = int(
                product.get(
                    "quantity",
                    0
                )
            )

            minimum = int(
                product.get(
                    "minimum_stock",
                    0
                )
            )


            if quantity == 0:

                status = "🔴 Out of Stock"

            elif quantity <= minimum:

                status = "🟡 Low Stock"

            else:

                status = "🟢 Available"


            table_data.append({

                "ID":
                    product_id,

                "Product":
                    product.get(
                        "name",
                        ""
                    ),

                "Category":
                    product.get(
                        "category",
                        ""
                    ),

                "Purchase":
                    f"₹{float(product.get('purchase_price',0)):.2f}",

                "Selling":
                    f"₹{float(product.get('selling_price',0)):.2f}",

                "Stock":
                    quantity,

                "Minimum":
                    minimum,

                "Status":
                    status
            })


        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "📦 No products available. "
            "Go to Add Product to create your first product."
        )

# ADD PRODUCT

elif menu == "➕ Add Product":

    st.header("➕ Add New Product")

    st.write(
        "Enter the product information below."
    )


    with st.form(
        "add_product_form"
    ):

        col1, col2 = st.columns(2)


        with col1:

            product_id = st.text_input(
                "Product ID",
                placeholder="Example: P001"
            )

            product_name = st.text_input(
                "Product Name",
                placeholder="Example: Laptop"
            )

            category = st.text_input(
                "Category",
                placeholder="Example: Electronics"
            )

            purchase_price = st.number_input(
                "Purchase Price",
                min_value=0.0,
                step=0.01
            )


        with col2:

            selling_price = st.number_input(
                "Selling Price",
                min_value=0.0,
                step=0.01
            )

            quantity = st.number_input(
                "Initial Stock",
                min_value=0,
                step=1
            )

            minimum_stock = st.number_input(
                "Minimum Stock Level",
                min_value=0,
                step=1
            )


        submit = st.form_submit_button(
            "➕ Add Product",
            use_container_width=True
        )


    if submit:

        product_id = product_id.strip()
        product_name = product_name.strip()
        category = category.strip()


        if not product_id:

            st.error(
                "❌ Product ID is required."
            )

        elif not product_name:

            st.error(
                "❌ Product Name is required."
            )

        elif not category:

            st.error(
                "❌ Category is required."
            )

        elif product_id in inventory:

            st.warning(
                "⚠️ Product ID already exists."
            )

        elif selling_price < purchase_price:

            st.error(
                "❌ Selling price cannot be lower than purchase price."
            )

        else:

            inventory[product_id] = {

                "name":
                    product_name,

                "category":
                    category,

                "purchase_price":
                    purchase_price,

                "selling_price":
                    selling_price,

                "quantity":
                    int(quantity),

                "minimum_stock":
                    int(minimum_stock)
            }


            save_json(
                INVENTORY_FILE,
                inventory
            )


            st.success(
                f"✅ {product_name} added successfully!"
            )

            st.rerun()
# VIEW PRODUCTS
elif menu == "📋 View Products":

    st.header("📋 Products")

    st.write(
        "All products currently available in inventory."
    )


    if inventory:

        table_data = []


        for product_id, product in inventory.items():

            quantity = int(
                product.get(
                    "quantity",
                    0
                )
            )

            minimum = int(
                product.get(
                    "minimum_stock",
                    0
                )
            )


            if quantity == 0:

                status = "🔴 Out of Stock"

            elif quantity <= minimum:

                status = "🟡 Low Stock"

            else:

                status = "🟢 Available"


            table_data.append({

                "Product ID":
                    product_id,

                "Product Name":
                    product.get(
                        "name",
                        ""
                    ),

                "Category":
                    product.get(
                        "category",
                        ""
                    ),

                "Purchase Price":
                    f"₹{float(product.get('purchase_price',0)):.2f}",

                "Selling Price":
                    f"₹{float(product.get('selling_price',0)):.2f}",

                "Stock":
                    quantity,

                "Minimum":
                    minimum,

                "Status":
                    status
            })


        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "📦 No products found."
        )

# UPDATE PRODUCT
elif menu == "✏️ Update Product":

    st.header("✏️ Update Product")


    if not inventory:

        st.info(
            "📦 No products available."
        )

    else:

        selected_id = st.selectbox(
            "Select Product",
            list(inventory.keys()),
            format_func=lambda x:
                f"{x} - {inventory[x].get('name','')}"
        )


        product = inventory[selected_id]


        with st.form(
            "update_product_form"
        ):

            col1, col2 = st.columns(2)


            with col1:

                new_name = st.text_input(
                    "Product Name",
                    value=product.get(
                        "name",
                        ""
                    )
                )

                new_category = st.text_input(
                    "Category",
                    value=product.get(
                        "category",
                        ""
                    )
                )

                new_purchase = st.number_input(
                    "Purchase Price",
                    min_value=0.0,
                    value=float(
                        product.get(
                            "purchase_price",
                            0
                        )
                    ),
                    step=0.01
                )


            with col2:

                new_selling = st.number_input(
                    "Selling Price",
                    min_value=0.0,
                    value=float(
                        product.get(
                            "selling_price",
                            0
                        )
                    ),
                    step=0.01
                )

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=int(
                        product.get(
                            "quantity",
                            0
                        )
                    ),
                    step=1
                )

                new_minimum = st.number_input(
                    "Minimum Stock",
                    min_value=0,
                    value=int(
                        product.get(
                            "minimum_stock",
                            0
                        )
                    ),
                    step=1
                )


            update = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )


        if update:

            if not new_name.strip():

                st.error(
                    "❌ Product name is required."
                )

            elif new_selling < new_purchase:

                st.error(
                    "❌ Selling price cannot be lower than purchase price."
                )

            else:

                inventory[selected_id] = {

                    "name":
                        new_name.strip(),

                    "category":
                        new_category.strip(),

                    "purchase_price":
                        new_purchase,

                    "selling_price":
                        new_selling,

                    "quantity":
                        int(new_quantity),

                    "minimum_stock":
                        int(new_minimum)
                }


                save_json(
                    INVENTORY_FILE,
                    inventory
                )


                st.success(
                    "✅ Product updated successfully!"
                )

                st.rerun()
# DELETE PRODUCT
elif menu == "🗑️ Delete Product":

    st.header("🗑️ Delete Product")


    if not inventory:

        st.info(
            "📦 No products available."
        )

    else:

        selected_id = st.selectbox(
            "Select Product",
            list(inventory.keys()),
            format_func=lambda x:
                f"{x} - {inventory[x].get('name','')}"
        )


        product = inventory[selected_id]


        st.warning(
            f"⚠️ You are about to delete "
            f"**{product.get('name','')}**"
        )


        confirm = st.checkbox(
            "I confirm that I want to delete this product."
        )


        if st.button(
            "🗑️ Delete Product",
            type="primary",
            use_container_width=True
        ):

            if not confirm:

                st.error(
                    "❌ Please confirm deletion."
                )

            else:

                name = product.get(
                    "name",
                    "Product"
                )


                del inventory[selected_id]


                save_json(
                    INVENTORY_FILE,
                    inventory
                )


                st.success(
                    f"✅ {name} deleted successfully!"
                )

                st.rerun()

# CUSTOMER SALE
elif menu == "🛒 Customer Sale":

    st.header("🛒 Customer Sale")

    st.write(
        "Create a customer bill and automatically update stock."
    )


    available = {

        product_id: product

        for product_id, product
        in inventory.items()

        if int(
            product.get(
                "quantity",
                0
            )
        ) > 0
    }


    if not available:

        st.error(
            "🚨 No products are currently available for sale."
        )

    else:

        selected_id = st.selectbox(
            "Select Product",
            list(available.keys()),
            format_func=lambda x:
                f"{x} - {available[x].get('name','')}"
        )


        product = inventory[selected_id]


        current_stock = int(
            product.get(
                "quantity",
                0
            )
        )


        purchase_price = float(
            product.get(
                "purchase_price",
                0
            )
        )
        selling_price = float(
            product.get(
                "selling_price",
                0
            )
        )
        col1, col2 = st.columns(2)
        with col1:
            customer = st.text_input(
                "Customer Name",
                placeholder="Walk-in Customer"
            )
            quantity_sold = st.number_input(
                "Quantity",
                min_value=1,
                max_value=current_stock,
                value=1,
                step=1
            )
        with col2:
            payment = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Card"
                ]
            )
        st.info(
            f"📦 Available Stock: **{current_stock}**"
        )
        total = (
            selling_price
            * int(quantity_sold)
        )
        profit = (
            selling_price
            - purchase_price
        ) * int(quantity_sold)
        st.divider()
        st.subheader("🧾 Bill Preview")
        bill_col1, bill_col2 = st.columns(2)
        with bill_col1:
            st.write(
                f"**Product:** {product.get('name','')}"
            )
            st.write(
                f"**Quantity:** {quantity_sold}"
            )
            st.write(
                f"**Unit Price:** ₹{selling_price:.2f}"
            )
        with bill_col2:
            st.write(
                f"**Customer:** "
                f"{customer if customer else 'Walk-in Customer'}"
            )
            st.write(
                f"**Payment:** {payment}"
            )
            st.markdown(
                f"### 💰 Total: ₹{total:,.2f}"
            )
        if st.button(
            "💳 Confirm Payment & Generate Bill",
            type="primary",
            use_container_width=True
        ):
            bill_number = (
                "BILL-"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )
            remaining_stock = (
                current_stock
                - int(quantity_sold)
            )
            # UPDATE STOCK
            inventory[selected_id]["quantity"] = (
                remaining_stock
            )
            # SALE RECORD
            sale = {
                "bill_number":
                    bill_number,
                "customer_name":
                    customer
                    if customer
                    else "Walk-in Customer",
                "product_id":
                    selected_id,
                "product_name":
                    product.get(
                        "name",
                        ""
                    ),
                "quantity":
                    int(quantity_sold),
                "selling_price":
                    selling_price,
                "purchase_price":
                    purchase_price,
                "total":
                    total,
                "profit":
                    profit,
                "payment_method":
                    payment,
                "date":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            }
            sales.append(
                sale
            )
            save_json(
                INVENTORY_FILE,
                inventory
            )
            save_json(
                SALES_FILE,
                sales
            )
            # BILL
            st.success(
                "✅ Payment successful!"
            )
            st.markdown(
                f"""
                <div class="bill-card">

                    <h2>🧾 INVOICE</h2>

                    <hr>

                    <p>
                    <b>Bill Number:</b>
                    {bill_number}
                    </p>

                    <p>
                    <b>Date:</b>
                    {sale['date']}
                    </p>

                    <p>
                    <b>Customer:</b>
                    {sale['customer_name']}
                    </p>

                    <p>
                    <b>Product:</b>
                    {sale['product_name']}
                    </p>

                    <p>
                    <b>Quantity:</b>
                    {sale['quantity']}
                    </p>

                    <p>
                    <b>Unit Price:</b>
                    ₹{sale['selling_price']:.2f}
                    </p>

                    <p>
                    <b>Payment:</b>
                    {sale['payment_method']}
                    </p>

                    <hr>

                    <div class="bill-total">
                    💰 Total Paid:
                    ₹{sale['total']:,.2f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")
            st.info(
                f"📦 Remaining Stock: "
                f"**{remaining_stock}**"
            )
            minimum = int(
                product.get(
                    "minimum_stock",
                    0
                )
            )
            if remaining_stock == 0:
                st.error(
                    f"🚨 OUT OF STOCK — "
                    f"{product.get('name','')}"
                )
            elif remaining_stock <= minimum:
                st.warning(
                    f"⚠️ LOW STOCK ALERT — "
                    f"{product.get('name','')} "
                    f"has only {remaining_stock} "
                    f"units remaining."
                )
            else:
                st.success(
                    "🟢 Stock level is normal."
                )
# SALES HISTORY
elif menu == "📊 Sales History":
    st.header("📊 Sales History")
    if not sales:
        st.info(
            "🧾 No sales recorded yet."
        )
    else:
        history = []
        for sale in reversed(sales):
            history.append({
                "Bill":
                    sale.get(
                        "bill_number",
                        ""
                    ),
                "Customer":
                    sale.get(
                        "customer_name",
                        ""
                    ),
                "Product":
                    sale.get(
                        "product_name",
                        ""
                    ),
                "Quantity":
                    sale.get(
                        "quantity",
                        0
                    ),
                "Total":
                    f"₹{float(sale.get('total',0)):.2f}",

                "Profit":
                    f"₹{float(sale.get('profit',0)):.2f}",

                "Payment":
                    sale.get(
                        "payment_method",
                        ""
                    ),
                "Date":
                    sale.get(
                        "date",
                        ""
                    )
            })
        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )
# STOCK ALERTS
elif menu == "🚨 Stock Alerts":
    st.header("🚨 Stock Alerts")
    alerts = []
    for product_id, product in inventory.items():
        quantity = int(
            product.get(
                "quantity",
                0
            )
        )
        minimum = int(
            product.get(
                "minimum_stock",
                0
            )
        )
        if quantity <= minimum:
            alerts.append(
                (
                    product_id,
                    product
                )
            )
    if not alerts:
        st.success(
            "🟢 All products have sufficient stock."
        )
    else:
        st.warning(
            f"⚠️ {len(alerts)} product(s) "
            f"need attention."
        )
        for product_id, product in alerts:
            name = product.get(
                "name",
                ""
            )
            quantity = int(
                product.get(
                    "quantity",
                    0
                )
            )
            minimum = int(
                product.get(
                    "minimum_stock",
                    0
                )
            )
            if quantity == 0:
                st.error(
                    f"🚨 {name} ({product_id}) "
                    f"OUT OF STOCK"
                )
            else:
                st.warning(
                    f"⚠️ {name} ({product_id}) "
                    f"Stock: {quantity} | "
                    f"Minimum: {minimum}"
                )
# FOOTER
st.divider()
st.markdown(
    """
    <div class="footer">
        📦 Inventory Pro &nbsp; | &nbsp;
        Smart Inventory Management System
    </div>
    """,
    unsafe_allow_html=True
)