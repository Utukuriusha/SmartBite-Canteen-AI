import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Hatch — Smart Canteen",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    :root {
        --chalk: #1F3329;
        --paper: #F3EEE3;
        --amber: #E2A33B;
        --tomato: #C1502E;
        --leaf: #4C7A54;
    }
    .main {
        background-color: var(--paper);
    }
    .stButton>button {
        background-color: var(--chalk);
        color: white;
        border-radius: 4px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #294238;
        color: white;
    }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--chalk);
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "menu" not in st.session_state:
    st.session_state.menu = [
        {"id": 1, "name": "Masala Dosa", "cat": "Breakfast", "veg": True, "price": 60, "desc": "Crisp rice-and-lentil crepe, spiced potato filling, coconut chutney and sambar.", "available": True, "emoji": "🥞"},
        {"id": 2, "name": "Idli Sambar", "cat": "Breakfast", "veg": True, "price": 45, "desc": "Four steamed rice cakes with sambar and coconut chutney.", "available": True, "emoji": "🥣"},
        {"id": 3, "name": "Bread Omelette", "cat": "Breakfast", "veg": False, "price": 50, "desc": "Two-egg onion omelette with toasted bread.", "available": True, "emoji": "🍳"},
        {"id": 4, "name": "Veg Thali", "cat": "Mains", "veg": True, "price": 90, "desc": "Dal, seasonal sabzi, rice, two rotis, salad and papad.", "available": True, "emoji": "🍱"},
        {"id": 5, "name": "Chicken Curry Rice", "cat": "Mains", "veg": False, "price": 110, "desc": "Home-style chicken curry served with steamed rice.", "available": True, "emoji": "🍛"},
        {"id": 6, "name": "Paneer Roll", "cat": "Mains", "veg": True, "price": 75, "desc": "Spiced paneer masala wrapped in a hot paratha.", "available": True, "emoji": "🌯"},
        {"id": 7, "name": "Egg Biryani", "cat": "Mains", "veg": False, "price": 95, "desc": "Fragrant rice layered with spiced egg, served with raita.", "available": True, "emoji": "🍚"},
        {"id": 8, "name": "Samosa (2 pcs)", "cat": "Snacks", "veg": True, "price": 25, "desc": "Potato and pea filling with tamarind chutney.", "available": True, "emoji": "🥟"},
        {"id": 9, "name": "Veg Cutlet", "cat": "Snacks", "veg": True, "price": 30, "desc": "Mixed vegetable patty with green chutney.", "available": True, "emoji": "🥙"},
        {"id": 10, "name": "Chicken Puff", "cat": "Snacks", "veg": False, "price": 35, "desc": "Flaky pastry with a spiced chicken filling.", "available": True, "emoji": "🥐"},
        {"id": 11, "name": "Filter Coffee", "cat": "Beverages", "veg": True, "price": 20, "desc": "South Indian filter coffee, served hot.", "available": True, "emoji": "☕"},
        {"id": 12, "name": "Masala Chai", "cat": "Beverages", "veg": True, "price": 15, "desc": "Spiced milk tea.", "available": True, "emoji": "🍵"},
        {"id": 13, "name": "Cold Coffee", "cat": "Beverages", "veg": True, "price": 40, "desc": "Iced coffee blended with milk and sugar.", "available": True, "emoji": "🥤"},
        {"id": 14, "name": "Fresh Lime Soda", "cat": "Beverages", "veg": True, "price": 30, "desc": "Lime, soda and mint, sweet or salted.", "available": True, "emoji": "🍋"},
        {"id": 15, "name": "Gulab Jamun (2 pcs)", "cat": "Desserts", "veg": True, "price": 30, "desc": "Warm milk dumplings in sugar syrup.", "available": True, "emoji": "🍮"},
        {"id": 16, "name": "Fruit Custard", "cat": "Desserts", "veg": True, "price": 35, "desc": "Chilled custard with seasonal fruit.", "available": True, "emoji": "🍨"}
    ]

if "orders" not in st.session_state:
    st.session_state.orders = [
        {"token": "H-49", "items": [{"id": 1, "name": "Masala Dosa", "price": 60, "qty": 1}], "total": 65, "status": "Preparing", "placedAt": datetime.now(), "mine": False},
        {"token": "H-48", "items": [{"id": 4, "name": "Veg Thali", "price": 90, "qty": 1}], "total": 95, "status": "Ready", "placedAt": datetime.now(), "mine": False}
    ]

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "token_counter" not in st.session_state:
    st.session_state.token_counter = 49

if "waste_records" not in st.session_state:
    st.session_state.waste_records = []

if "admin_authed" not in st.session_state:
    st.session_state.admin_authed = False

CART_FEE = 5
ADMIN_PASSCODE = "hatch2026"

# --- Sidebar Navigation ---
st.sidebar.markdown("# 🍲 HATCH")
st.sidebar.markdown("*Smart Canteen Dashboard*")
nav_selection = st.sidebar.radio("Navigation", ["Home & Live Queue", "Browse Menu & Cart", "My Orders", "Staff Dashboard"])

st.sidebar.markdown("---")
cart_count = sum(st.session_state.cart.values())
st.sidebar.info(f"🛒 Cart Items: **{cart_count}**")

# ==================== HOME & LIVE QUEUE ====================
if nav_selection == "Home & Live Queue":
    st.markdown("### Campus food, without the queue")
    st.title("Order ahead.\nSkip the queue.\nGrab it hot.")
    st.write("Hatch lets you browse today's canteen menu, place your order securely, and walk up to the hatch only when your token is called.")

    st.markdown("---")
    st.subheader("🔴 Live Hatch Board")
    
    if not st.session_state.orders:
        st.write("No active orders in the queue.")
    else:
        for order in st.session_state.orders[:6]:
            cols = st.columns([1, 2, 1])
            with cols[0]:
                st.markdown(f"### `{order['token']}`")
            with cols[1]:
                item_summary = ", ".join([f"{i['qty']}× {i['name']}" for i in order['items']])
                st.write(item_summary)
            with cols[2]:
                status_color = "🟢" if order['status'] == "Ready" else "🟡"
                st.markdown(f"**{status_color} {order['status']}**")
            st.markdown("---")

# ==================== BROWSE MENU & CART ====================
elif nav_selection == "Browse Menu & Cart":
    st.title("🍽️ Today's Menu")
    st.write("Find your favorite meal, add it to your cart, and place your order instantly.")

    # Search & Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("Search menu", placeholder="Search items...")
    with col2:
        categories = ["All", "Breakfast", "Mains", "Snacks", "Beverages", "Desserts"]
        selected_cat = st.selectbox("Category", categories)
    with col3:
        veg_only = st.checkbox("🌱 Veg only")

    st.markdown("---")

    # Display Menu Grid
    filtered_menu = st.session_state.menu
    if selected_cat != "All":
        filtered_menu = [m for m in filtered_menu if m["cat"] == selected_cat]
    if veg_only:
        filtered_menu = [m for m in filtered_menu if m["veg"]]
    if search_query:
        filtered_menu = [m for m in filtered_menu if search_query.lower() in m["name"].lower() or search_query.lower() in m["desc"].lower()]

    if not filtered_menu:
        st.warning("No menu items match your search criteria.")
    
    grid_cols = st.columns(3)
    for idx, item in enumerate(filtered_menu):
        with grid_cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']} {item['name']}")
                st.caption(f"{'🟢 Vegetarian' if item['veg'] else '🔴 Non-Veg'} | **₹{item['price']}**")
                st.write(item['desc'])
                
                if item['available']:
                    qty_key = f"qty_{item['id']}"
                    qty = st.number_input("Qty", min_value=1, max_value=10, value=1, key=qty_key, label_visibility="collapsed")
                    if st.button(f"Add to Cart (₹{item['price'] * qty})", key=f"add_{item['id']}"):
                        st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + qty
                        st.success(f"Added {qty}x {item['name']} to cart!")
                else:
                    st.error("Sold Out")

    st.markdown("---")
    st.subheader("🛒 Your Cart Summary")
    if not st.session_state.cart:
        st.info("Your cart is empty. Add items from the menu above.")
    else:
        subtotal = 0
        for item_id, qty in list(st.session_state.cart.items()):
            item = next((m for m in st.session_state.menu if m["id"] == item_id), None)
            if item:
                item_total = item["price"] * qty
                subtotal += item_total
                col_c1, col_c2, col_c3 = st.columns([3, 1, 1])
                with col_c1:
                    st.write(f"**{item['name']}** (₹{item['price']} × {qty})")
                with col_c2:
                    st.write(f"**₹{item_total}**")
                with col_c3:
                    if st.button("❌", key=f"del_{item_id}"):
                        del st.session_state.cart[item_id]
                        st.rerun()

        total = subtotal + CART_FEE
        st.write(f"Subtotal: **₹{subtotal}** | Packaging Fee: **₹{CART_FEE}**")
        st.markdown(f"### Grand Total: ₹{total}")

        if st.button("🚀 Place Order Now", type="primary", use_container_width=True):
            order_items = []
            for item_id, qty in st.session_state.cart.items():
                item = next((m for m in st.session_state.menu if m["id"] == item_id), None)
                if item:
                    order_items.append({"id": item["id"], "name": item["name"], "price": item["price"], "qty": qty})
            
            st.session_state.token_counter += 1
            new_token = f"H-{st.session_state.token_counter}"
            
            new_order = {
                "token": new_token,
                "items": order_items,
                "total": total,
                "status": "Placed",
                "placedAt": datetime.now(),
                "mine": True
            }
            st.session_state.orders.insert(0, new_order)
            st.session_state.cart = {}
            st.success(f"Order placed successfully! Your digital token is **{new_token}**.")
            st.balloons()

# ==================== MY ORDERS ====================
elif nav_selection == "My Orders":
    st.title("🎫 My Digital Order Tickets")
    st.write("Keep this token handy when you collect your order at the hatch.")

    my_orders = [o for o in st.session_state.orders if o.get("mine")]
    if not my_orders:
        st.info("You haven't placed any orders yet from this session.")
    else:
        for order in my_orders:
            with st.container(border=True):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"## Token: `{order['token']}`")
                    st.caption(f"Placed at: {order['placedAt'].strftime('%H:%M:%S')}")
                with c2:
                    status_badge = f"🟡 {order['status']}" if order['status'] != "Ready" else "🟢 Ready"
                    st.markdown(f"### {status_badge}")
                
                st.markdown("---")
                for item in order['items']:
                    st.write(f"- {item['qty']} × {item['name']} — ₹{item['price'] * item['qty']}")
                st.write(f"**Total Paid: ₹{order['total']}** (incl. packaging fee)")

# ==================== STAFF DASHBOARD ====================
elif nav_selection == "Staff Dashboard":
    st.title("🔐 Kitchen Staff Dashboard")
    
    if not st.session_state.admin_authed:
        passcode = st.text_input("Enter Staff Passcode", type="password")
        if st.button("Sign In"):
            if passcode == ADMIN_PASSCODE:
                st.session_state.admin_authed = True
                st.success("Access granted!")
                st.rerun()
            else:
                st.error("Incorrect passcode. (Hint: hatch2026)")
    else:
        if st.button("Sign Out"):
            st.session_state.admin_authed = False
            st.rerun()

        st.markdown("---")
        admin_tab = st.selectbox("Dashboard Views", ["Output Overview", "Live Order Queue", "Menu Management", "Food Waste Tracking", "Demand Forecast"])

        if admin_tab == "Output Overview":
            st.subheader("📊 Output & Operations Overview")
            total_orders = len(st.session_state.orders)
            revenue = sum(o["total"] for o in st.session_state.orders)
            in_kitchen = len([o for o in st.session_state.orders if o["status"] == "Preparing"])
            ready = len([o for o in st.session_state.orders if o["status"] == "Ready"])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Orders", total_orders)
            col2.metric("Revenue", f"₹{revenue}")
            col3.metric("In Kitchen", in_kitchen)
            col4.metric("Ready for Pickup", ready)

        elif admin_tab == "Live Order Queue":
            st.subheader("⚡ Manage Order Queue")
            if not st.session_state.orders:
                st.write("No orders in queue.")
            else:
                for idx, order in enumerate(st.session_state.orders):
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        st.write(f"**{order['token']}**")
                    with c2:
                        st.write(", ".join([f"{i['qty']}× {i['name']}" for i in order['items']]))
                    with c3:
                        new_status = st.selectbox("Status", ["Placed", "Preparing", "Ready"], index=["Placed", "Preparing", "Ready"].index(order['status']), key=f"status_{idx}")
                        if new_status != order['status']:
                            order['status'] = new_status
                            st.rerun()
                    st.markdown("---")

        elif admin_tab == "Menu Management":
            st.subheader("🍔 Menu Availability & Items")
            for idx, item in enumerate(st.session_state.menu):
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.write(f"**{item['emoji']} {item['name']}** (₹{item['price']})")
                with c2:
                    avail = st.toggle("Available", value=item['available'], key=f"avail_{item['id']}")
                    if avail != item['available']:
                        item['available'] = avail
                        st.rerun()
                with c3:
                    if st.button("Delete", key=f"del_menu_{item['id']}"):
                        st.session_state.menu = [m for m in st.session_state.menu if m["id"] != item["id"]]
                        st.rerun()

        elif admin_tab == "Food Waste Tracking":
            st.subheader("♻️ Food Waste Records")
            with st.form("waste_form"):
                w_date = st.date_input("Service Date")
                w_item = st.selectbox("Food Item", [m['name'] for m in st.session_state.menu])
                w_prep = st.number_input("Prepared Portions", min_value=0, step=1)
                w_sold = st.number_input("Sold Portions", min_value=0, step=1)
                w_waste = st.number_input("Wasted Portions", min_value=0, step=1)
                submitted = st.form_submit_button("Save Waste Record")
                if submitted:
                    st.session_state.waste_records.append({"date": str(w_date), "item": w_item, "prepared": w_prep, "sold": w_sold, "wasted": w_waste})
                    st.success("Waste record saved successfully!")

            if st.session_state.waste_records:
                st.dataframe(pd.DataFrame(st.session_state.waste_records))

        elif admin_tab == "Demand Forecast":
            st.subheader("📈 7-Day Moving Average Demand Forecast")
            forecast_data = []
            for item in st.session_state.menu:
                item_waste = [w for w in st.session_state.waste_records if w["item"] == item["name"]]
                avg_sold = sum([w["sold"] for w in item_waste]) / len(item_waste) if item_waste else 25
                forecast_data.append({"Food Item": item["name"], "Category": item["cat"], "Suggested Portions": int(avg_sold * 1.1)})
            st.table(pd.DataFrame(forecast_data))
