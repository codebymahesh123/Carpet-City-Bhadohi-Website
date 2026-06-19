import streamlit as st
import qrcode
import io
from urllib.parse import quote
from supabase import create_client, Client

# --- SUPABASE CONNECTION ---
# YAHAN APNI SUPABASE DETAILS DALEIN (Project Settings -> API se copy karein)
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Supabase connection error: {e}")

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="Carpet City Bhadohi Rugs", 
    page_icon=r"D:\The carpet city\98be94da-f811-45d0-b5e0-54e6ddc53a7d.jpg", 
    layout="wide"
)

# --- THEME TOGGLE (Dark/Light Mode) ---
st.sidebar.markdown("### 🎨 Theme Settings")
is_dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode", value=False)

if is_dark_mode:
    bg_color = "#0e1117"
    card_bg = "#262730"
    text_color = "#fafafa"
    title_color = "#ff6666" 
    subtitle_color = "#cccccc"
    price_color = "#ff9999"
    border_color = "#ff6666"
else:
    bg_color = "#f7f9fa"
    card_bg = "#ffffff"
    text_color = "#000000"
    title_color = "#8B0000"
    subtitle_color = "#555555"
    price_color = "#B22222"
    border_color = "#8B0000"

# Premium Custom Dynamic CSS
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        color: {text_color};
    }}
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}
    .title-text {{
        color: {title_color};
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }}
    .subtitle-text {{
        color: {subtitle_color};
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }}
    .product-card {{
        background-color: {card_bg};
        color: {text_color};
        padding: 15px;
        border-radius: 0px 0px 10px 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-top: 3px solid {border_color};
    }}
    .price-text {{
        color: {price_color};
        font-weight: bold;
        font-size: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Navigation Menu
menu = ["🛍️ Product Catalog", "🛒 Shopping Cart & Checkout", "⚙️ Admin Panel (Add New Rug)"]

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

# 4. Sidebar Navigation & WhatsApp Contact
st.sidebar.markdown("---")
current_index = menu.index(st.session_state.page)
choice = st.sidebar.selectbox("Go to Page", menu, index=current_index)

if choice != st.session_state.page:
    st.session_state.page = choice
    st.rerun()

# --- WHATSAPP CONTACT SECTION ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact Us")
YOUR_WHATSAPP_NUMBER = "918009076300"
wa_link = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text=Hello,%20I%20want%20to%20know%20more%20about%20your%20carpets!"

st.sidebar.markdown(f"""
    <a href="{wa_link}" target="_blank" style="text-decoration: none;">
        <button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; display: flex; align-items: center; justify-content: center; font-size: 16px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="24" style="margin-right: 10px;"> 
            Chat on WhatsApp
        </button>
    </a>
""", unsafe_allow_html=True)


# 5. Header
st.markdown("<h1 class='title-text'>👑 SM Carpet City Bhadohi Rugs</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Bhadohi Ke Premium Online Store</p>", unsafe_allow_html=True)


# --- PAGE 1: PRODUCT CATALOG ---
if st.session_state.page == "🛍️ Product Catalog":
    st.subheader("Our Premium Products")
    
    if not st.session_state.products:
        st.info("No products found in the database.")
    else:
        cols = st.columns(3)
        for idx, prod in enumerate(st.session_state.products):
            with cols[idx % 3]:
                if not prod.get('image_path'):
                    st.warning("📸 Image placeholder")
                else:
                    try: 
                        st.image(prod['image_path'], use_container_width=True)
                    except: 
                        st.error("Image load nahi ho saki")
                
                st.markdown(f"""
                    <div class='product-card'>
                        <h3 style="margin-top:0px;">{prod['name']}</h3>
                        <p>{prod['description']}</p>
                        <p class='price-text'>₹{prod['price']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"Add to Cart 🛒", key=f"add_{prod['id']}"):
                        prod_id = prod['id']
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]['quantity'] += 1
                        else:
                            st.session_state.cart[prod_id] = {'name': prod['name'], 'price': prod['price'], 'quantity': 1}
                        st.success("Cart me add ho gaya!")
                
                with btn_col2:
                    if st.button(f"Buy Now ⚡", key=f"buy_{prod['id']}", type="primary"):
                        prod_id = prod['id']
                        if prod_id in st.session_state.cart:
                            st.session_state.cart[prod_id]['quantity'] += 1
                        else:
                            st.session_state.cart[prod_id] = {'name': prod['name'], 'price': prod['price'], 'quantity': 1}
                        st.session_state.page = "🛒 Shopping Cart & Checkout"
                        st.rerun()


# --- PAGE 2: CART & CHECKOUT ---
elif st.session_state.page == "🛒 Shopping Cart & Checkout":
    st.subheader("Cart Checkout Details")
    
    if not st.session_state.cart:
        st.info("Cart is Empty")
    else:
        total_amount = 0
        st.markdown("### Selected Items:")
        
        for p_id, item in list(st.session_state.cart.items()):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            col1.write(item['name'])
            col2.write(f"₹{item['price']}")
            
            new_qty = col3.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{p_id}")
            st.session_state.cart[p_id]['quantity'] = new_qty
            total_amount += item['price'] * new_qty
            
            if col4.button("Remove ❌", key=f"rem_{p_id}"):
                del st.session_state.cart[p_id]
                st.rerun()
                
        st.markdown(f"## **Total Amount: ₹{total_amount}**")
        st.markdown("---")
        st.markdown("### 🚚 Delivery & Payment Details")
        
        with st.form("checkout_form"):
            customer_name = st.text_input("Full Name *")
            phone = st.text_input("Mobile Number *")
            address = st.text_area("Full Delivery Address *")
            home_address = st.text_area("Enter your Home address")
            pincode = st.text_input("PIN Code *", max_chars=6)
            
            submit_order = st.form_submit_button("Proceed to Pay via UPI 💳")
            
            if submit_order:
                if not customer_name or not phone or not address or not pincode:
                    st.error("Please enter Right Information!")
                elif not phone.isdigit() or len(phone) != 10:
                    st.error("Please enter a 10-digit phone number")
                elif not pincode.isdigit() or len(pincode) != 6:
                    st.error("Please enter a 6-digit PIN Code !")
                else:
                    st.session_state.order_ready = {
                        "name": customer_name,
                        "amount": total_amount,
                        "phone": phone,
                        "address": address,
                        "home_addreses" : home_address,
                        "pincode": pincode,
                    }

        # --- DYNAMIC UPI QR CODE & DATABASE SAVE ---
        if 'order_ready' in st.session_state:
            st.markdown("---")
            st.success(f"Your Delivery details have been submitted {st.session_state.order_ready['name']}. Contact for me!!")
            
            YOUR_UPI_ID = "maheshsing221314-4@okhdfcbank" 
            YOUR_NAME = "MAHESH MAURYA"
            
            tn_note = quote(f"Order for {st.session_state.order_ready['name']}")
            pn_name = quote(YOUR_NAME)
            upi_url = f"upi://pay?pa={YOUR_UPI_ID}&pn={pn_name}&am={st.session_state.order_ready['amount']}&cu=INR&tn={tn_note}"
            
            st.markdown("### 📱 Scan QR Code to Pay")
            st.info(f"Amount to Pay: ₹{st.session_state.order_ready['amount']}")
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(upi_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            col_qr, col_btn = st.columns([1, 2])
            with col_qr:
                st.image(byte_im, width=250, caption="Scan using PhonePe, GPay, Paytm etc.")
            
            with col_btn:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown(f'<a href="{upi_url}" target="_blank"><button style="background-color:#8B0000; color:white; padding:12px 24px; border:none; border-radius:5px; font-size:18px; cursor:pointer; font-weight:bold;">Pay via UPI App (Click Here) 🚀</button></a>', unsafe_allow_html=True)
                st.write("Click here to payment by GooglePay and PhonePay other")
            
            if st.button("Your Payment has been Pending !!"):
                try:
                    # DATABASE ME ORDER SAVE KARNA
                    order_data = {
                        "customer_name": st.session_state.order_ready['name'],
                        "phone": st.session_state.order_ready['phone'],
                        "address": st.session_state.order_ready['address'],
                        "home_address": st.session_state.order_ready['home_addreses'],
                        "pincode": st.session_state.order_ready['pincode'],
                        "total_amount": int(st.session_state.order_ready['amount']),
                        "payment_status": "Pending"
                    }
                    supabase.table("orders").insert(order_data).execute()
                    
                    st.balloons()
                    st.success("Thank you! Your order has been saved to the Database. I will contact you.")
                    st.session_state.cart = {}
                    del st.session_state.order_ready
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save order in Database: {e}")


# --- PAGE 3: ADMIN PANEL ---
elif st.session_state.page == "⚙️ Admin Panel (Add New Rug)":
    st.subheader("Admin Dashboard - New stock add here !!")
    
    with st.form("add_product_form"):
        new_name = st.text_input("Dari / Rug Name")
        new_price = st.number_input("Price (₹)", min_value=0, value=0)
        new_desc = st.text_area("Product Description")
        new_img_path = st.text_input("Image File Path or URL", value="")
        
        submit_new_prod = st.form_submit_button("Add Product to Catalog")
        
        if submit_new_prod:
            if new_name == "": 
                st.error("Enter the product name !")
            else:
                try:
                    # DATABASE ME NAYA PRODUCT ADD KARNA
                    product_data = {
                        "name": new_name,
                        "price": int(new_price),
                        "description": new_desc,
                        "image_path": new_img_path
                    }
                    supabase.table("products").insert(product_data).execute()
                    
                    st.success(f"Naya Product '{new_name}' Database me add ho gaya!")
                    # List update karne ke liye rerun karte hain
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding product to Database: {e}")