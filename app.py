import streamlit as st
import qrcode
import io
from urllib.parse import quote
from supabase import create_client, Client

# --- SUPABASE CONNECTION ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Supabase connection error: {e}")

# 1. Page Configuration
st.set_page_config(
    page_title="Carpet City Bhadohi Rugs", 
    page_icon="👑", # Local path hatakar emoji lagaya hai taaki live app crash na ho
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar by default band rahega clean look ke liye
)

# 2. Always Light Mode & Flipkart Style CSS
st.markdown("""
    <style>
    /* Background and General Text */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f3f6; /* Flipkart grey background */
        color: #212121;
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    /* Top Bar Title */
    .brand-title {
        color: #2874f0; /* Flipkart Blue */
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
    /* Product Card */
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
""", unsafe_allow_html=True)

# 3. Session State Initialization
if 'page' not in st.session_state:
    st.session_state.page = "🛍️ Product Catalog"

if 'cart' not in st.session_state:
    st.session_state.cart = {}

# DATABASE SE PRODUCTS FETCH KARNA
try:
    response = supabase.table("products").select("*").order("id").execute()
    st.session_state.products = response.data
except Exception as e:
    st.error("Database se products load nahi ho paye!")
    st.session_state.products = []

# --- TOP NAVIGATION BAR (Flipkart Style) ---
nav_col1, nav_col2, nav_col3 = st.columns([3, 1, 1])

with nav_col1:
    st.markdown("<div class='brand-title'>👑 SM Carpet City</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-subtitle'>Explore Premium Bhadohi Rugs</div>", unsafe_allow_html=True)

with nav_col2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🛍️ Product Catalog"
        st.rerun()

with nav_col3:
    cart_items = sum(item['quantity'] for item in st.session_state.cart.values())
    if st.button(f"🛒 Cart ({cart_items})", use_container_width=True, type="primary"):
        st.session_state.page = "🛒 Shopping Cart & Checkout"
        st.rerun()

st.markdown("---")


# 4. Sidebar Navigation (Only for Admin & Contact)
st.sidebar.markdown("### ⚙️ Quick Links")
if st.sidebar.button("Admin Panel (Add Rug)", use_container_width=True):
    st.session_state.page = "⚙️ Admin Panel"
    st.rerun()
# --- FLOATING WHATSAPP BUTTON (Bottom-Right) ---
YOUR_WHATSAPP_NUMBER = "918009076300"
wa_link = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text=Hello,%20I%20want%20to%20know%20more%20about%20your%20carpets!"

st.markdown(f"""
    <style>
    .floating-wa-button {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
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
""", unsafe_allow_html=True) 



# --- PAGE 1: PRODUCT CATALOG ---
if st.session_state.page == "🛍️ Product Catalog":
    
    if not st.session_state.products:
        st.info("No products found in the database.")
    else:
        # 3 columns for laptop, automatically stacks on mobile
        cols = st.columns(3)
        for idx, prod in enumerate(st.session_state.products):
            with cols[idx % 3]:
                st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                
                # Image
                if not prod.get('image_path'):
                    st.warning("📸 No Image")
                else:
                    try: 
                        st.image(prod['image_path'], use_container_width=True)
                    except: 
                        st.error("Image error")
                
                # Details
                st.markdown(f"""
                    <div class='product-title'>{prod['name']}</div>
                    <div class='product-desc'>{prod['description']}</div>
                    <div class='price-text'>₹{prod['price']}</div>
                """, unsafe_allow_html=True)
                
                # Buttons (Flipkart Colors using Streamlit UI)
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("Cart 🛒", key=f"add_{prod['id']}", use_container_width=True):
                        prod_id = prod['id']
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]['quantity'] += 1
                        else:
                            st.session_state.cart[prod_id] = {'name': prod['name'], 'price': prod['price'], 'quantity': 1}
                        st.toast("🛒 Added to Cart!")
                
                with btn_col2:
                    # 'primary' type gives it a solid color highlight
                    if st.button("Buy ⚡", key=f"buy_{prod['id']}", use_container_width=True, type="primary"):
                        prod_id = prod['id']
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]['quantity'] += 1
                        else:
                            st.session_state.cart[prod_id] = {'name': prod['name'], 'price': prod['price'], 'quantity': 1}
                        st.session_state.page = "🛒 Shopping Cart & Checkout"
                        st.rerun()
                        
                st.markdown("</div>", unsafe_allow_html=True)


# --- PAGE 2: CART & CHECKOUT ---
elif st.session_state.page == "🛒 Shopping Cart & Checkout":
    
    if not st.session_state.cart:
        st.info("Your Cart is Empty. Please add items from the Home page.")
    else:
        col_cart, col_summary = st.columns([2, 1])
        
        total_amount = 0
        
        with col_cart:
            st.markdown("### 🛒 My Cart")
            for p_id, item in list(st.session_state.cart.items()):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.write(f"**{item['name']}**")
                c2.write(f"₹{item['price']}")
                
                new_qty = c3.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{p_id}", label_visibility="collapsed")
                st.session_state.cart[p_id]['quantity'] = new_qty
                total_amount += item['price'] * new_qty
                
                if c4.button("🗑️", key=f"rem_{p_id}"):
                    del st.session_state.cart[p_id]
                    st.rerun()
                    
            st.markdown("---")
            st.markdown(f"### **Total Amount: ₹{total_amount}**")
            
        with col_summary:
            st.markdown("### 🚚 Delivery Details")
            with st.form("checkout_form"):
                customer_name = st.text_input("Full Name *")
                phone = st.text_input("Mobile Number *")
                address = st.text_area("Full Delivery Address *")
                pincode = st.text_input("PIN Code *", max_chars=6)
                
                submit_order = st.form_submit_button("Proceed to Pay", type="primary", use_container_width=True)
                
                if submit_order:
                    if not customer_name or not phone or not address or not pincode:
                        st.error("Please fill all required fields!")
                    elif not phone.isdigit() or len(phone) != 10:
                        st.error("Please enter a valid 10-digit phone number")
                    elif not pincode.isdigit() or len(pincode) != 6:
                        st.error("Please enter a valid 6-digit PIN Code")
                    else:
                        st.session_state.order_ready = {
                            "name": customer_name,
                            "amount": total_amount,
                            "phone": phone,
                            "address": address,
                            "pincode": pincode,
                        }

        # --- DYNAMIC UPI QR CODE & DATABASE SAVE ---
        if 'order_ready' in st.session_state:
            st.markdown("---")
            st.success(f"Delivery details saved for {st.session_state.order_ready['name']}. Please complete payment.")
            
            YOUR_UPI_ID = "maheshsing221314-4@okhdfcbank" 
            YOUR_NAME = "MAHESH MAURYA"
            
            tn_note = quote(f"Order for {st.session_state.order_ready['name']}")
            pn_name = quote(YOUR_NAME)
            upi_url = f"upi://pay?pa={YOUR_UPI_ID}&pn={pn_name}&am={st.session_state.order_ready['amount']}&cu=INR&tn={tn_note}"
            
            st.markdown("### 📱 Payment Options")
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
                
                st.image(byte_im, width=200, caption="Scan via PhonePe, GPay, Paytm")
            
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<a href="{upi_url}" target="_blank"><button style="background-color:#2874f0; color:white; padding:12px 24px; border:none; border-radius:5px; font-size:16px; cursor:pointer; font-weight:bold; width:100%;">Pay via UPI App (Click Here) 🚀</button></a>', unsafe_allow_html=True)
                st.write("Click above if paying from mobile.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Confirm Payment Completed ✅", use_container_width=True, type="primary"):
                    try:
                        order_data = {
                            "customer_name": st.session_state.order_ready['name'],
                            "phone": st.session_state.order_ready['phone'],
                            "address": st.session_state.order_ready['address'],
                            "home_address": "N/A", # Optional field removed for cleaner UI
                            "pincode": st.session_state.order_ready['pincode'],
                            "total_amount": int(st.session_state.order_ready['amount']),
                            "payment_status": "Pending"
                        }
                        supabase.table("orders").insert(order_data).execute()
                        
                        st.balloons()
                        st.success("Thank you! Your order has been placed. We will contact you soon.")
                        st.session_state.cart = {}
                        del st.session_state.order_ready
                    except Exception as e:
                        st.error(f"Failed to save order in Database: {e}")


# --- PAGE 3: ADMIN PANEL ---
elif st.session_state.page == "⚙️ Admin Panel":
    st.subheader("Admin Dashboard - Add New Stock")
    
    with st.form("add_product_form"):
        new_name = st.text_input("Dari / Rug Name")
        new_price = st.number_input("Price (₹)", min_value=0, value=0)
        new_desc = st.text_area("Product Description")
        new_img_path = st.text_input("Image File Path or URL (e.g. from Supabase Storage)", value="")
        
        submit_new_prod = st.form_submit_button("Add Product to Catalog", type="primary")
        
        if submit_new_prod:
            if new_name == "": 
                st.error("Enter the product name!")
            else:
                try:
                    product_data = {
                        "name": new_name,
                        "price": int(new_price),
                        "description": new_desc,
                        "image_path": new_img_path
                    }
                    supabase.table("products").insert(product_data).execute()
                    
                    st.success(f"Naya Product '{new_name}' Database me add ho gaya!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding product to Database: {e}")
