import io
from urllib.parse import quote
import qrcode
import streamlit as st
from supabase import Client, create_client

# --- 1. PAGE CONFIGURATION (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="Carpet City Bhadohi Rugs",
    page_icon="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/WhatsApp%20Image%202026-07-31%20at%202.45.21%20PM.jpeg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. HIDE STREAMLIT BRANDING & LIGHT MODE STYLES ---
st.markdown(
    """
    <style>
    /* Hide Default Header, Footer, and Toolbar */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden;}
    
    [data-testid="stAppDeployButton"] {display: none !important; visibility: hidden !important;}
    [class^="viewerBadge"] {display: none !important; visibility: hidden !important;}
    [class^="stDeployButton"] {display: none !important; visibility: hidden !important;}
    [data-testid="stToolbar"] {display: none !important; visibility: hidden !important;}
    a[href^="https://streamlit.io/cloud"] {display: none !important;}

    /* Light Mode Custom Styling (Flipkart Theme) */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f3f6;
        color: #212121;
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    .brand-title {
        color: #2874f0;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
        font-size: 32px;
        margin-top: -15px;
        margin-bottom: 5px;
    }
    .brand-subtitle {
        color: #878787;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 4px;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,.08);
        margin-bottom: 20px;
        text-align: center;
        transition: box-shadow 0.3s;
    }
    .product-card:hover {
        box-shadow: 0 4px 12px 0 rgba(0,0,0,.15);
    }
    .product-title {
        font-size: 16px;
        font-weight: 600;
        color: #212121;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .product-desc {
        font-size: 13px;
        color: #878787;
        margin-bottom: 10px;
    }
    .price-text {
        color: #212121;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 3. SUPABASE CONNECTION ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")


@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Supabase connection error: {e}")

# --- 4. SESSION STATE INITIALIZATION ---
if "page" not in st.session_state:
    st.session_state.page = "🛍️ Product Catalog"

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "cart" not in st.session_state:
    st.session_state.cart = {}

# FETCH PRODUCTS FROM DATABASE
try:
    response = supabase.table("products").select("*").order("id").execute()
    st.session_state.products = response.data
except Exception as e:
    st.error("Database connection issue! Unable to load products.")
    st.session_state.products = []

# --- 5. TOP NAVIGATION BAR ---
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 1, 1, 1])

with nav_col1:
    st.markdown(
        """
        <div class='brand-title'>
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/WhatsApp%20Image%202026-07-31%20at%202.45.21%20PM.jpeg" width="40" height="40" style="vertical-align: middle; margin-right: 8px; border-radius: 4px; margin-bottom: 4px;"> 
            SM Carpet City
        </div>
        <div class='brand-subtitle'>Explore Premium Bhadohi Rugs</div>
    """,
        unsafe_allow_html=True,
    )

with nav_col2:
    if st.button("⚙️ Admin", use_container_width=True):
        st.session_state.page = "⚙️ Admin Panel"
        st.rerun()

with nav_col3:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🛍️ Product Catalog"
        st.rerun()

with nav_col4:
    cart_items = sum(
        item["quantity"] for item in st.session_state.cart.values()
    )
    if st.button(
        f"🛒 Cart ({cart_items})", use_container_width=True, type="primary"
    ):
        st.session_state.page = "🛒 Shopping Cart & Checkout"
        st.rerun()

st.markdown("---")

# --- 6. SIDEBAR NAVIGATION ---
st.sidebar.markdown("### ⚙️ Quick Links")
if st.sidebar.button("Admin Panel (Add Rug)", use_container_width=True):
    st.session_state.page = "⚙️ Admin Panel"
    st.rerun()

# --- 7. FLOATING WHATSAPP BUTTON ---
YOUR_WHATSAPP_NUMBER = "918009076300"
wa_link = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text=Hello,%20I%20want%20to%20know%20more%20about%20your%20carpets!"

st.markdown(
    f"""
    <style>
    .floating-wa-button {{
        position: fixed;
        bottom: 80px;
        right: 20px;
        z-index: 999999;
    }}
    .wa-btn {{
        background-color: #25D366;
        color: white;
        border: none;
        padding: 15px;
        border-radius: 50px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s;
    }}
    .wa-btn:hover {{
        transform: scale(1.1);
    }}
    </style>
    
    <div class="floating-wa-button">
        <a href="{wa_link}" target="_blank">
            <button class="wa-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="30">
            </button>
        </a>
    </div>
""",
    unsafe_allow_html=True,
)


# --- PAGE 1: PRODUCT CATALOG ---
if st.session_state.page == "🛍️ Product Catalog":
    if not st.session_state.products:
        st.info("No products found in the database.")
    else:
        cols = st.columns(3)
        for idx, prod in enumerate(st.session_state.products):
            with cols[idx % 3]:
                st.markdown(
                    "<div class='product-card'>", unsafe_allow_html=True
                )

                if not prod.get("image_path"):
                    st.warning("📸 No Image Available")
                else:
                    try:
                        st.image(prod["image_path"], use_container_width=True)
                    except Exception:
                        st.error("Image failed to load")

                st.markdown(
                    f"""
                    <div class='product-title'>{prod['name']}</div>
                    <div class='product-desc'>{prod['description']}</div>
                    <div class='price-text'>₹{prod['price']}</div>
                """,
                    unsafe_allow_html=True,
                )

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(
                        "Cart 🛒",
                        key=f"add_{prod['id']}",
                        use_container_width=True,
                    ):
                        prod_id = prod["id"]
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]["quantity"] += 1
                        else:
                            st.session_state.cart[prod_id] = {
                                "name": prod["name"],
                                "price": prod["price"],
                                "quantity": 1,
                            }
                        st.toast("🛒 Added to Cart!")

                with btn_col2:
                    if st.button(
                        "Buy ⚡",
                        key=f"buy_{prod['id']}",
                        use_container_width=True,
                        type="primary",
                    ):
                        prod_id = prod["id"]
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]["quantity"] += 1
                        else:
                            st.session_state.cart[prod_id] = {
                                "name": prod["name"],
                                "price": prod["price"],
                                "quantity": 1,
                            }
                        st.session_state.page = "🛒 Shopping Cart & Checkout"
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)


# --- PAGE 2: CART & CHECKOUT ---
elif st.session_state.page == "🛒 Shopping Cart & Checkout":
    if "order_ready" in st.session_state:
        st.success(
            f"✅ Order Confirmed for {st.session_state.order_ready['name']}! Delivery details saved."
        )

        YOUR_UPI_ID = "maheshsing221314-3@okaxis"
        YOUR_NAME = "MAHESH MAURYA"

        tn_note = quote(f"Order for {st.session_state.order_ready['name']}")
        pn_name = quote(YOUR_NAME)
        upi_url = f"upi://pay?pa={YOUR_UPI_ID}&pn={pn_name}&am={st.session_state.order_ready['amount']}&cu=INR&tn={tn_note}"

        st.markdown("### 📱 Complete Your Payment")
        st.info(f"Amount to Pay: ₹{st.session_state.order_ready['amount']}")

        col_qr, col_btn = st.columns([1, 2])
        with col_qr:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(upi_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.image(
                byte_im, width=200, caption="Scan via PhonePe, GPay, Paytm"
            )

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<a href="{upi_url}" target="_blank"><button style="background-color:#2874f0; color:white; padding:12px 24px; border:none; border-radius:5px; font-size:16px; cursor:pointer; font-weight:bold; width:100%;">Pay via UPI App (Click Here) 🚀</button></a>',
                unsafe_allow_html=True,
            )
            st.write("Click above if paying from mobile.")

            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Shop More 🛍️", use_container_width=True):
                del st.session_state.order_ready
                st.session_state.page = "🛍️ Product Catalog"
                st.rerun()

    elif not st.session_state.cart:
        st.info(
            "Your Cart is Empty. Please add items from the Product Catalog."
        )

    else:
        col_cart, col_summary = st.columns([2, 1])
        total_amount = 0

        with col_cart:
            st.markdown("# 🛒 My Cart")
            for p_id, item in list(st.session_state.cart.items()):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.write(f"**{item['name']}**")
                c2.write(f"₹{item['price']}")

                new_qty = c3.number_input(
                    "Qty",
                    min_value=1,
                    value=item["quantity"],
                    key=f"qty_{p_id}",
                    label_visibility="collapsed",
                )
                st.session_state.cart[p_id]["quantity"] = new_qty
                total_amount += item["price"] * new_qty

                if c4.button("🗑️", key=f"rem_{p_id}"):
                    del st.session_state.cart[p_id]
                    st.rerun()

            st.markdown("---")
            st.markdown(f"### **Total Amount: ₹{total_amount}**")

        with col_summary:
            st.markdown("### 🚚 Delivery Details")
            with st.form("checkout_form"):
                customer_name = st.text_input(
                    "Full Name *", placeholder="e.g., Rahul Sharma"
                )
                phone = st.text_input(
                    "Mobile Number *", placeholder="e.g., 9876543210"
                )
                address = st.text_area(
                    "Full Delivery Address *",
                    placeholder="House/Flat No., Building Name, Street, Landmark, City...",
                    height=100,
                )
                pincode = st.text_input(
                    "PIN Code *", max_chars=6, placeholder="e.g., 221401"
                )

                submit_order = st.form_submit_button(
                    "Proceed to Pay 🚀", type="primary", use_container_width=True
                )

                if submit_order:
                    if (
                        not customer_name
                        or not phone
                        or not address
                        or not pincode
                    ):
                        st.error("Please fill all required fields!")
                    elif not phone.isdigit() or len(phone) != 10:
                        st.error("Please enter a valid 10-digit phone number")
                    elif not pincode.isdigit() or len(pincode) != 6:
                        st.error("Please enter a valid 6-digit PIN Code")
                    else:
                        order_data = {
                            "customer_name": customer_name,
                            "phone": phone,
                            "address": address,
                            "home_address": "N/A",
                            "pincode": pincode,
                            "total_amount": int(total_amount),
                            "payment_status": "Pending",
                        }

                        try:
                            with st.spinner(
                                "🔒 Securing connection & generating your order..."
                            ):
                                import time

                                time.sleep(1.5)

                                supabase.table("orders").insert(
                                    order_data
                                ).execute()

                                st.session_state.order_ready = {
                                    "name": customer_name,
                                    "amount": total_amount,
                                    "phone": phone,
                                    "address": address,
                                    "pincode": pincode,
                                }
                                st.session_state.cart = {}

                            st.toast(
                                "📦 Order initialized successfully!", icon="🚀"
                            )
                            st.rerun()

                        except Exception as e:
                            st.error(f"Failed to save order in Database: {e}")


# --- PAGE 3: ADMIN PANEL ---
elif st.session_state.page == "⚙️ Admin Panel":
    if not st.session_state.admin_logged_in:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0d0d0d !important;
                background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000000 100%);
                color: #00ffcc !important;
            }
            .cyber-box {
                background: rgba(10, 25, 47, 0.8);
                border: 2px solid #00ffcc;
                box-shadow: 0 0 15px #00ffcc, inset 0 0 10px #00ffcc;
                border-radius: 10px;
                padding: 40px;
                max-width: 450px;
                margin: auto;
                text-align: center;
                margin-top: 50px;
            }
            .cyber-title {
                color: #ff007f;
                font-family: 'Courier New', Courier, monospace;
                font-size: 30px;
                font-weight: bold;
                text-shadow: 0 0 10px #ff007f;
                margin-bottom: 20px;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='cyber-box'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='cyber-title'>[ SYSTEM_ACCESS ]</div>",
            unsafe_allow_html=True,
        )

        admin_user = st.text_input("USER ID", placeholder="Enter Username")
        admin_pass = st.text_input(
            "PASSWORD", type="password", placeholder="Enter Password"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "INITIALIZE LOGIN ⚡", use_container_width=True, type="primary"
        ):
            if admin_user and admin_pass:
                try:
                    response = (
                        supabase.table("admins")
                        .select("*")
                        .eq("username", admin_user)
                        .eq("password", admin_pass)
                        .execute()
                    )

                    if len(response.data) > 0:
                        st.session_state.admin_logged_in = True
                        st.success("ACCESS GRANTED. Welcome to Mainframe.")
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED: Invalid Credentials!")
                except Exception as e:
                    st.error(
                        f"SYSTEM ERROR: Could not connect to Auth Database. {e}"
                    )
            else:
                st.warning("Please provide complete credentials.")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <style>
            .stApp { 
                background-color: #f8f9fa !important; 
                color: #2b2b2b !important; 
            }
            [data-testid="stForm"] {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
                border: 1px solid #eaeaea;
            }
            [data-testid="stFormSubmitButton"] button {
                background-color: #4CAF50 !important;
                color: white !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                padding: 10px 24px !important;
                border: none !important;
                transition: 0.3s !important;
            }
            [data-testid="stFormSubmitButton"] button:hover {
                background-color: #45a049 !important;
                box-shadow: 0px 4px 12px rgba(76, 175, 80, 0.3) !important;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("## ⚙️ Admin Dashboard")
            st.markdown(
                "<p style='color: #666; margin-top: -15px;'>Manage your Dari/Rug catalog efficiently.</p>",
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("Logout 🔴", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.divider()

        with st.form("add_product_form", clear_on_submit=True):
            st.markdown("### ✨ Add New Product")
            st.markdown("<br>", unsafe_allow_html=True)

            row1_col1, row1_col2 = st.columns(2)

            with row1_col1:
                new_name = st.text_input(
                    "Dari / Rug Name *",
                    placeholder="e.g., Persian Floral Silk Rug",
                )

            with row1_col2:
                new_price = st.number_input(
                    "Price (₹) *",
                    min_value=0,
                    value=None,
                    placeholder="e.g., 2500",
                )

            new_img_path = st.text_input(
                "Image File Path or URL",
                placeholder="https://your-supabase.com/.../rug-image.jpg",
                help="Paste the direct URL of the image uploaded to your Supabase storage.",
            )

            new_desc = st.text_area(
                "Product Description",
                placeholder="Briefly describe material, colors, dimensions...",
                height=120,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_new_prod = st.form_submit_button(
                "➕ Add Product to Catalog"
            )

            if submit_new_prod:
                if not new_name or new_price is None:
                    st.warning(
                        "⚠️ Please fill in all mandatory fields (Name and Price)!"
                    )
                else:
                    try:
                        product_data = {
                            "name": new_name,
                            "price": int(new_price),
                            "description": new_desc,
                            "image_path": new_img_path,
                        }
                        supabase.table("products").insert(
                            product_data
                        ).execute()
                        st.success(
                            f"✅ Successfully added **{new_name}** to your catalog!"
                        )
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error adding product to Database: {e}")

# --- 8. FOOTER RENDER ---
trusted_light_footer = """
<style>
.trust-footer {
    background-color: #ffffff;
    color: #475569;
    padding: 60px 40px 20px 40px;
    font-family: 'Arial', sans-serif;
    margin-top: 80px;
    border-top: 4px solid #2874f0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.04);
    width: 100%;
}
.tf-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    max-width: 1200px;
    margin: 0 auto;
    gap: 30px;
}
.tf-col {
    flex: 1;
    min-width: 220px;
}
.tf-col h4 {
    color: #0f172a;
    margin-bottom: 20px;
    font-size: 18px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tf-col p {
    font-size: 14px;
    line-height: 1.8;
    color: #475569;
}
.tf-col a {
    color: #64748b;
    text-decoration: none;
    font-size: 15px;
    line-height: 2.2;
    display: flex;
    align-items: center;
    transition: color 0.3s ease;
}
.tf-col a::before {
    content: '▸';
    margin-right: 8px;
    color: #2874f0;
    font-size: 18px;
}
.tf-col a:hover {
    color: #2874f0;
    font-weight: 600;
}
.trust-badges {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 700;
    color: #16a34a;
    background: #f0fdf4;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #bbf7d0;
}
.tf-bottom {
    text-align: left;
    padding-top: 25px;
    border-top: 1px solid #e2e8f0;
    margin-top: 40px;
    font-size: 13px;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}
.tf-bottom b {
    color: #334155;
}
.secure-payments {
    font-size: 20px;
    letter-spacing: 8px;
}
</style>

<div class="trust-footer">
    <div class="tf-container">
        <div class="tf-col">
            <h4>SM Carpet City</h4>
            <p>Premium Rugs & Carpets straight from the weavers of Bhadohi. Delivering quality and authenticity globally.</p>
            <div class="trust-badges">
                <div class="badge">🔒 100% Secure Checkout</div>
                <div class="badge">✅ Verified Premium Seller</div>
            </div>
        </div>
        <div class="tf-col">
            <h4>Quick Links</h4>
            <a href="#">Shop All Rugs</a>
            <a href="#">Track Your Order</a>
            <a href="#">Help & Support</a>
            <a href="#">About Us</a>
        </div>
        <div class="tf-col">
            <h4>Legal & Policies</h4>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms & Conditions</a>
            <a href="#">Return & Refund Policy</a>
            <a href="#">Secure Payment Policy</a>
        </div>
        <div class="tf-col">
            <h4>Contact Us</h4>
            <p>📍 Sector 11, Main Market,<br>Bhadohi, UP - 221401</p>
            <p>📞 +91-8009076300</p>
            <p>✉️ support@smcarpetcity.com</p>
        </div>
    </div>
    <div class="tf-bottom">
        <span>© 2026-2027 <b>SM Carpet City</b>. All Rights Reserved. | Protected & Secured.</span>
        <span class="secure-payments">💳 🏦 📱</span>
    </div>
</div>
"""

st.markdown(trusted_light_footer, unsafe_allow_html=True)
