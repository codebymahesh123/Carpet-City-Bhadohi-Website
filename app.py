import io
import time
import random
from datetime import datetime
from urllib.parse import quote
import qrcode
import streamlit as st
from supabase import Client, create_client

# ==============================================================================
# 1. PAGE CONFIGURATION (MUST BE FIRST)
# ==============================================================================
st.set_page_config(
    page_title="SM Carpet City || Handcrafted Rugs & Carpets",
    page_icon="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/WhatsApp%20Image%202026-07-31%20at%202.45.21%20PM.jpeg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# 2. GLOBAL STYLES & FONTS (FLIPKART / AMAZON THEME)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography - Safely applied without breaking icon ligatures */
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Form controls & Button text */
    input, textarea, select, 
    [data-testid="stButton"] button p,
    [data-testid="stButton"] button div,
    [data-testid="stTab"] button p,
    [data-testid="stExpander"] summary span p,
    [data-testid="stExpander"] summary span div {
        font-family: 'Poppins', sans-serif !important;
    }

    /* PRESERVE STREAMLIT MATERIAL ICONS & FIX EXPANDER ARROW BUG */
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    [data-testid="stExpanderToggleIcon"] span,
    [data-testid="stExpanderToggleIcon"] svg,
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    span[data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] * {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        word-wrap: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
    }

    /* Clean UI Overrides */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    [class^="viewerBadge"] { display: none !important; }
    [class^="stDeployButton"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }

    /* App Background */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f3f6;
        color: #1e293b;
    }
    
    /* Buttons */
    [data-testid="stButton"] button {
        border-radius: 8px !important;
        transition: all 0.25s ease !important;
        font-weight: 600 !important;
    }
    [data-testid="stButton"] button[kind="primary"] {
        background-color: #fb641b !important; /* Flipkart Orange for Primary CTA */
        color: white !important;
        border: none !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #e5530d !important;
        box-shadow: 0 4px 14px rgba(251, 100, 27, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Brand Header */
    .brand-title {
        color: #2874f0; /* Flipkart Royal Blue */
        font-weight: 800;
        font-size: 28px;
        margin-top: -10px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        text-decoration: none;
    }

    /* Product Cards (Flipkart/Amazon Style) */
    .product-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e5e7eb;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        transform: translateY(-4px);
        border-color: #cbd5e1;
    }
    .product-title {
        font-size: 15px;
        font-weight: 600;
        color: #212121;
        margin-top: 10px;
        margin-bottom: 4px;
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 40px;
    }
    .product-desc {
        font-size: 12px;
        color: #717478;
        margin-bottom: 8px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 34px;
    }
    
    /* FLIPKART & AMAZON PRICING ROW */
    .price-row-fk {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 8px;
        margin-top: 6px;
        margin-bottom: 2px;
        flex-wrap: wrap;
    }
    .selling-price {
        color: #212121;
        font-weight: 800;
        font-size: 20px;
    }
    .mrp-price {
        color: #878787;
        text-decoration: line-through;
        font-size: 13px;
        font-weight: 500;
    }
    .discount-percent {
        color: #388e3c; /* Flipkart Green */
        font-weight: 700;
        font-size: 14px;
        letter-spacing: -0.2px;
    }
    
    /* BADGES */
    .discount-ribbon {
        background: #388e3c;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        letter-spacing: 0.3px;
    }
    .save-tag {
        color: #2e7d32;
        font-size: 11px;
        font-weight: 600;
        background: #e8f5e9;
        border: 1px dashed #a5d6a7;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 4px;
        margin-bottom: 8px;
    }
    .assured-badge {
        font-size: 11px;
        font-weight: 700;
        color: #2874f0;
        font-style: italic;
    }
    
    .rating-container {
        font-size: 13px;
        margin-bottom: 4px;
    }
    .stars { color: #f59e0b; }
    .reviews-count { color: #878787; font-size: 12px; }
    
    /* Order Status Badges */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .status-pending { background-color: #fef3c7; color: #b45309; }
    .status-confirmed { background-color: #dbeafe; color: #1d4ed8; }
    .status-dispatched { background-color: #ede9fe; color: #6d28d9; }
    .status-delivered { background-color: #dcfce7; color: #15803d; }
    .status-cancelled { background-color: #fee2e2; color: #b91c1c; }

    /* Order Card Container */
    .order-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. SUPABASE CONNECTION
# ==============================================================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

@st.cache_resource
def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.warning("⚠️ Supabase credentials not found in st.secrets. Using local mock mode.")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Supabase connection error: {e}")
    supabase = None

# ==============================================================================
# 4. SESSION STATE INITIALIZATION
# ==============================================================================
if "page" not in st.session_state:
    st.session_state.page = "🛍️ Product Catalog"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "carousel_idx" not in st.session_state:
    st.session_state.carousel_idx = 0
if "applied_coupon" not in st.session_state:
    st.session_state.applied_coupon = None

# Fetch Products from DB
if "products" not in st.session_state:
    if supabase:
        with st.spinner("⏳ Fetching premium rugs from Bhadohi catalog..."):
            try:
                response = supabase.table("products").select("*").order("id").execute()
                st.session_state.products = response.data if response.data else []
            except Exception as e:
                st.error(f"Database issue: {e}")
                st.session_state.products = []
    else:
        st.session_state.products = [
            {
                "id": 1,
                "name": "Kashmir Royal Silk Persian Rug (5x8 ft)",
                "price": 4250,
                "mrp": 8500,  # 50% Off
                "description": "Authentic hand-knotted pure Mulberry silk rug with traditional floral medallion pattern.",
                "image_path": "https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=600&q=80",
                "category": "Silk Rugs"
            },
            {
                "id": 2,
                "name": "Bhadohi Hand-Tufted Wool Carpet",
                "price": 3780,
                "mrp": 4200,  # 10% Off
                "description": "Thick, plush 100% New Zealand blend wool carpet. Soft underfoot and durable.",
                "image_path": "https://images.unsplash.com/photo-1579656381226-5fc0f0100c3b?auto=format&fit=crop&w=600&q=80",
                "category": "Wool Rugs"
            },
            {
                "id": 3,
                "name": "Boho Natural Jute & Cotton Dari",
                "price": 925,
                "mrp": 1850,  # 50% Off
                "description": "Eco-friendly natural woven jute runner with geometric fringe accents for living room.",
                "image_path": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?auto=format&fit=crop&w=600&q=80",
                "category": "Jute & Dari"
            }
        ]

# ==============================================================================
# 5. HELPER FUNCTIONS & FLIPKART/AMAZON PRICING ENGINE
# ==============================================================================
def get_pricing_details(prod):
    """Calculates Selling Price, MRP, Discount % (10% to 50%), and Savings like Flipkart & Amazon."""
    price = int(prod.get("price", 0))
    if prod.get("mrp") and int(prod["mrp"]) > price:
        mrp = int(prod["mrp"])
        discount_pct = int(round(((mrp - price) / mrp) * 100))
    else:
        p_id = prod.get("id", 1)
        discount_tiers = [50, 10, 40, 50, 20, 10, 50, 30, 15, 50]
        idx = (int(p_id) if str(p_id).isdigit() else 1) % len(discount_tiers)
        discount_pct = discount_tiers[idx]
        mrp = int(round(price / (1 - (discount_pct / 100))))
        if mrp > 100:
            mrp = (mrp // 100) * 100 + 99

    savings = max(0, mrp - price)
    return price, mrp, discount_pct, savings

def add_to_cart(prod):
    prod_id = str(prod["id"])
    price, mrp, discount_pct, savings = get_pricing_details(prod)
    if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["quantity"] += 1
    else:
        st.session_state.cart[prod_id] = {
            "id": prod["id"],
            "name": prod["name"],
            "price": price,
            "mrp": mrp,
            "discount_pct": discount_pct,
            "image_path": prod.get("image_path", ""),
            "quantity": 1,
        }

def render_product_card(prod, key_prefix=""):
    random.seed(prod["id"])
    rating = round(random.uniform(4.2, 5.0), 1)
    reviews = random.randint(35, 480)
    stars_html = f"<span class='stars'>{'★' * int(rating)}{'☆' * (5 - int(rating))}</span>"
    
    price, mrp, discount_pct, savings = get_pricing_details(prod)

    st.markdown("<div class='product-card'>", unsafe_allow_html=True)
    if not prod.get("image_path"):
        st.info("📸 Image Preview Unavailable")
    else:
        try:
            st.image(prod["image_path"], use_container_width=True)
        except Exception:
            st.error("Image loading failed")
            
    card_html = (
        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-top:4px;'>"
        f"<span class='discount-ribbon'>⚡ {discount_pct}% OFF</span>"
        f"<span class='assured-badge'>✓ Assured</span>"
        f"</div>"
        f"<div class='product-title'>{prod['name']}</div>"
        f"<div class='rating-container'>{stars_html} <span class='reviews-count'>{rating} ({reviews} ratings)</span></div>"
        f"<div class='product-desc'>{prod.get('description', 'Handcrafted masterpiece straight from the artisans.')}</div>"
        f"<div class='price-row-fk'>"
        f"<span class='selling-price'>₹{price:,}</span>"
        f"<span class='mrp-price'>₹{mrp:,}</span>"
        f"<span class='discount-percent'>{discount_pct}% off</span>"
        f"</div>"
        f"<div class='save-tag'>You Save: ₹{savings:,}</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Add to Cart 🛒", key=f"add_{key_prefix}_{prod['id']}", use_container_width=True):
            add_to_cart(prod)
            st.toast(f"🛒 Added '{prod['name'][:20]}...' to cart!")
    with btn_col2:
        if st.button("Buy Now ⚡", key=f"buy_{key_prefix}_{prod['id']}", use_container_width=True, type="primary"):
            add_to_cart(prod)
            st.session_state.page = "🛒 Shopping Cart & Checkout"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_status_badge(status):
    status_map = {
        "Pending": ("status-pending", "⏳ Pending Payment / Verification"),
        "Paid / Confirmed": ("status-confirmed", "✅ Payment Verified & Order Confirmed"),
        "Dispatched": ("status-dispatched", "🚚 In Transit (Dispatched)"),
        "Delivered": ("status-delivered", "🎉 Delivered Successfully"),
        "Cancelled": ("status-cancelled", "❌ Cancelled"),
    }
    css_class, label = status_map.get(status, ("status-pending", status))
    return f"<span class='status-badge {css_class}'>{label}</span>"

# ==============================================================================
# 6. TOP NAVIGATION BAR
# ==============================================================================
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([3.5, 1.2, 1.2, 1.2, 1.2])

with nav_col1:
    st.markdown("""
        <div class='brand-title'>
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/WhatsApp%20Image%202026-07-31%20at%202.45.21%20PM.jpeg" width="42" height="42" style="border-radius: 8px; margin-right: 12px; object-fit: cover;"> 
            SM Carpet City
        </div>
    """, unsafe_allow_html=True)

with nav_col2:
    if st.button("🏠 Catalog", use_container_width=True):
        st.session_state.page = "🛍️ Product Catalog"
        st.rerun()

with nav_col3:
    if st.button("📦 Track Order", use_container_width=True):
        st.session_state.page = "📦 Track Order"
        st.rerun()

with nav_col4:
    cart_count = sum(item["quantity"] for item in st.session_state.cart.values())
    if st.button(f"🛒 Cart ({cart_count})", use_container_width=True, type="primary"):
        st.session_state.page = "🛒 Shopping Cart & Checkout"
        st.rerun()

with nav_col5:
    if st.button("⚙️ Admin", use_container_width=True):
        st.session_state.page = "⚙️ Admin Panel"
        st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# ==============================================================================
# 7. FLOATING WHATSAPP BUTTON
# ==============================================================================
YOUR_WHATSAPP_NUMBER = "918009076300"
wa_link = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text=Hello%20SM%20Carpet%20City,%20I%20am%20interested%20in%20your%20carpets%20catalog!"
st.markdown(
    f"""
    <style>
    .floating-wa-button {{
        position: fixed;
        bottom: 30px;
        right: 25px;
        z-index: 999999;
    }}
    .wa-btn {{
        background-color: #25D366;
        color: white;
        border: none;
        padding: 14px;
        border-radius: 50%;
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.4);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }}
    .wa-btn:hover {{
        transform: scale(1.12);
        box-shadow: 0 8px 24px rgba(37, 211, 102, 0.6);
    }}
    </style>
    
    <div class="floating-wa-button">
        <a href="{wa_link}" target="_blank">
            <button class="wa-btn" title="Chat on WhatsApp">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="32" height="32" alt="WhatsApp">
            </button>
        </a>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# PAGE 1: PRODUCT CATALOG (FLIPKART / AMAZON STYLE OFFERS)
# ==============================================================================
if st.session_state.page == "🛍️ Product Catalog":
    if not st.session_state.products:
        st.info("No carpets currently available. Please check back shortly or contact us on WhatsApp!")
    else:
        # Grand Sale Banner (Flipkart Big Billion / Amazon Great Indian Festival Style)
        st.markdown("""
            <div style='background: linear-gradient(90deg, #2874f0 0%, #174ea6 100%); color: white; padding: 14px 20px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
                <div>
                    <b style='font-size: 18px;'>🎉 MEGA CARPET FESTIVAL SALE</b><br>
                    <span style='font-size: 13px; opacity: 0.9;'>Up to <b>50% OFF</b> + Extra 10% OFF with Coupon <b>CARPET10</b></span>
                </div>
                <div style='background: #fb641b; color: white; font-weight: 800; padding: 6px 14px; border-radius: 6px; font-size: 13px; margin-top: 5px;'>
                    LIMITED TIME DEALS ⚡
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Featured Collections Carousel
        st.markdown("### 🌟 Deal of the Day (Handpicked Highlights)")
        featured = st.session_state.products[:6]
        
        if len(featured) > 0:
            c_prev, c_cards, c_next = st.columns([0.6, 10, 0.6])
            with c_prev:
                st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)
                if st.button("◀", key="prev_btn", use_container_width=True):
                    st.session_state.carousel_idx = (st.session_state.carousel_idx - 1) % len(featured)
                    st.rerun()
            with c_cards:
                display_qty = min(3, len(featured))
                f_cols = st.columns(display_qty)
                for i in range(display_qty):
                    prod_idx = (st.session_state.carousel_idx + i) % len(featured)
                    with f_cols[i]:
                        render_product_card(featured[prod_idx], key_prefix=f"feat_{prod_idx}")
            with c_next:
                st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)
                if st.button("▶", key="next_btn", use_container_width=True):
                    st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % len(featured)
                    st.rerun()

        st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

        # Search, Category Filter, and Price Slider
        st.markdown("### 🏷️ All Rugs, Carpets & Hand-Woven Dari")
        f_col1, f_col2, f_col3 = st.columns([2.5, 1.5, 1.5])
        
        with f_col1:
            search_query = st.text_input("🔍 Search by rug name, style, or material...", placeholder="e.g. Persian, Silk, Wool, Kashmiri, Floral")
            
        with f_col2:
            sort_by = st.selectbox("Sort Order", ["Featured", "Price: Low to High", "Price: High to Low", "Biggest Discount (% Off)"])

        with f_col3:
            prices = [p["price"] for p in st.session_state.products if "price" in p and isinstance(p["price"], (int, float))]
            max_p = max(prices) if prices else 10000
            price_limit = st.slider("Max Budget (₹)", min_value=500, max_value=int(max_p), value=int(max_p), step=500)

        # Filter Logic
        filtered_prods = [
            p for p in st.session_state.products 
            if (search_query.lower() in p.get('name', '').lower() or search_query.lower() in p.get('description', '').lower())
            and p.get('price', 0) <= price_limit
        ]

        if sort_by == "Price: Low to High":
            filtered_prods = sorted(filtered_prods, key=lambda x: x.get('price', 0))
        elif sort_by == "Price: High to Low":
            filtered_prods = sorted(filtered_prods, key=lambda x: x.get('price', 0), reverse=True)
        elif sort_by == "Biggest Discount (% Off)":
            filtered_prods = sorted(filtered_prods, key=lambda x: get_pricing_details(x)[2], reverse=True)

        if not filtered_prods:
            st.warning("No carpets match your filter criteria. Try expanding your budget or search query.")
        else:
            st.caption(f"Showing **{len(filtered_prods)}** handcrafted items with special discount pricing")
            cols = st.columns(3)
            for idx, prod in enumerate(filtered_prods):
                with cols[idx % 3]:
                    render_product_card(prod, key_prefix="catalog")

# ==============================================================================
# PAGE 2: ORDER TRACKING
# ==============================================================================
elif st.session_state.page == "📦 Track Order":
    st.markdown("## 📦 Track Your Order Status")
    st.markdown("Enter your registered **Mobile Number** or **Order ID** to view live dispatch and delivery updates.")
    
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        track_input = st.text_input("Enter 10-Digit Mobile Number or Order ID", placeholder="e.g. 9876543210 or 1024")
    with t_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_track = st.button("Search Order 🔎", type="primary", use_container_width=True)

    if track_input or search_track:
        if supabase:
            with st.spinner("Searching records..."):
                query = supabase.table("orders").select("*")
                if track_input.isdigit() and len(track_input) <= 6:
                    query = query.eq("id", int(track_input))
                else:
                    query = query.eq("phone", track_input.strip())
                
                res = query.order("id", desc=True).execute()
                orders = res.data if res.data else []
        else:
            orders = [
                {
                    "id": 1042,
                    "customer_name": "Rajesh Kumar",
                    "phone": track_input,
                    "address": "B-42 Sector 5, Carpet City",
                    "pincode": "221314",
                    "total_amount": 4250,
                    "payment_status": "Dispatched",
                    "created_at": "2026-08-16T11:20:00"
                }
            ]

        if orders:
            st.markdown(f"#### Found **{len(orders)}** matching order(s):")
            for ord_data in orders:
                st.markdown(f"""
                    <div class='order-box'>
                        <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 12px;'>
                            <div>
                                <b style='font-size: 18px; color: #0f172a;'>Order #{ord_data.get('id')}</b>
                                <span style='color: #64748b; font-size: 13px; margin-left: 10px;'>Recipient: {ord_data.get('customer_name')}</span>
                            </div>
                            <div>
                                {render_status_badge(ord_data.get('payment_status', 'Pending'))}
                            </div>
                        </div>
                        <div style='display: flex; justify-content: space-between; flex-wrap: wrap; font-size: 14px;'>
                            <div>
                                📍 <b>Delivery Address:</b> {ord_data.get('address')}, PIN: <b>{ord_data.get('pincode')}</b><br>
                                📞 <b>Phone:</b> {ord_data.get('phone')}
                            </div>
                            <div style='text-align: right;'>
                                💰 <b>Total Bill:</b> <span style='color:#2874f0; font-weight:800; font-size:16px;'>₹{ord_data.get('total_amount', 0):,}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No orders found matching your input. Please check the mobile number or contact support.")

# ==============================================================================
# PAGE 3: SHOPPING CART & CHECKOUT (FLIPKART / AMAZON BILL BREAKDOWN)
# ==============================================================================
elif st.session_state.page == "🛒 Shopping Cart & Checkout":
    if "order_ready" in st.session_state:
        order_info = st.session_state.order_ready
        st.success(f"🎉 Order Registered for **{order_info['name']}**! (Order #{order_info.get('order_id', 'Pending')})")
        
        YOUR_UPI_ID = "maheshsing221314-3@okaxis"
        YOUR_NAME = "SM CARPET CITY"
        tn_note = quote(f"Order {order_info.get('order_id', '')} - {order_info['name']}")
        pn_name = quote(YOUR_NAME)
        upi_url = f"upi://pay?pa={YOUR_UPI_ID}&pn={pn_name}&am={order_info['amount']}&cu=INR&tn={tn_note}"
        
        st.markdown("### 📱 Complete Your UPI Payment")
        st.info(f"Final Payable Amount: **₹{order_info['amount']:,}** (Free Insured Delivery Included)")
        
        col_qr, col_pay_actions = st.columns([1, 1.8], gap="large")
        with col_qr:
            qr = qrcode.QRCode(version=1, box_size=8, border=3)
            qr.add_data(upi_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#0f172a", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), width=220, caption="Scan with GPay / PhonePe / Paytm")
            
        with col_pay_actions:
            st.markdown(
                f'<a href="{upi_url}" target="_blank"><button style="background-color:#2874f0; color:white; padding:14px 20px; border:none; border-radius:8px; font-size:16px; cursor:pointer; font-weight:700; width:100%; margin-bottom:12px;">⚡ Open in UPI App (GPay / PhonePe / Paytm)</button></a>',
                unsafe_allow_html=True,
            )
            
            # WhatsApp confirmation share link
            wa_order_text = quote(
                f"Hello SM Carpet City, I have placed Order #{order_info.get('order_id')} for ₹{order_info['amount']}.\nName: {order_info['name']}\nPhone: {order_info['phone']}\nAddress: {order_info['address']}, {order_info['pincode']}"
            )
            wa_confirm_url = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text={wa_order_text}"
            
            st.markdown(
                f'<a href="{wa_confirm_url}" target="_blank"><button style="background-color:#16a34a; color:white; padding:12px 20px; border:none; border-radius:8px; font-size:15px; cursor:pointer; font-weight:600; width:100%;">💬 Share Receipt on WhatsApp</button></a>',
                unsafe_allow_html=True,
            )
            
            st.markdown("---")
            st.markdown("##### 📝 Payment Verification (UTR / Reference No.)")
            with st.form("utr_form"):
                utr_num = st.text_input("Enter 12-Digit UPI Transaction ID / UTR:", placeholder="e.g. 423589123456")
                submit_utr = st.form_submit_button("Confirm Payment Done ✅", type="primary")
                if submit_utr:
                    if len(utr_num.strip()) < 6:
                        st.error("Please enter a valid reference / UTR number.")
                    else:
                        if supabase and order_info.get("order_id"):
                            try:
                                supabase.table("orders").update({
                                    "payment_status": f"Paid / Confirmed (UTR: {utr_num})",
                                    "home_address": f"UTR: {utr_num}"
                                }).eq("id", order_info["order_id"]).execute()
                                st.success("Thank you! Payment Reference submitted. We will dispatch your rug soon.")
                            except Exception as e:
                                st.error(f"Error submitting UTR: {e}")
                        else:
                            st.success("UTR Reference submitted!")

            if st.button("← Back to Product Catalog", use_container_width=True):
                del st.session_state.order_ready
                st.session_state.page = "🛍️ Product Catalog"
                st.rerun()

    elif not st.session_state.cart:
        st.info("🛒 Your cart is currently empty. Explore our catalog and grab up to 50% OFF deals!")
        if st.button("Explore Catalog 🛍️", type="primary"):
            st.session_state.page = "🛍️ Product Catalog"
            st.rerun()
    else:
        col_cart, col_summary = st.columns([1.6, 1.2], gap="large")
        total_mrp = 0
        total_selling_price = 0
        
        with col_cart:
            st.markdown("### 🛒 My Shopping Bag")
            for p_id, item in list(st.session_state.cart.items()):
                c1, c2, c3, c4 = st.columns([3, 1.4, 1.2, 0.8])
                c1.markdown(f"**{item['name']}**<br><span style='color:#388e3c; font-size:12px; font-weight:700;'>⚡ {item.get('discount_pct', 20)}% OFF</span>", unsafe_allow_html=True)
                c2.markdown(f"<span style='font-size:15px; font-weight:700;'>₹{item['price']:,}</span> <span style='text-decoration:line-through; color:#878787; font-size:12px;'>₹{item.get('mrp', item['price']):,}</span>", unsafe_allow_html=True)
                new_qty = c3.number_input(
                    "Qty", min_value=1, max_value=20, value=item["quantity"], key=f"qty_{p_id}", label_visibility="collapsed"
                )
                st.session_state.cart[p_id]["quantity"] = new_qty
                total_selling_price += item["price"] * new_qty
                total_mrp += item.get("mrp", item["price"]) * new_qty
                if c4.button("🗑️", key=f"rem_{p_id}"):
                    del st.session_state.cart[p_id]
                    st.rerun()
            
            st.markdown("---")
            
            # Coupon / Discount Code Feature
            st.markdown("##### 🎟️ Apply Promo / Coupon Code")
            coup_col1, coup_col2 = st.columns([2, 1])
            with coup_col1:
                coupon_input = st.text_input("Coupon Code", placeholder="e.g. CARPET10, BHADOHI500", label_visibility="collapsed")
            with coup_col2:
                if st.button("Apply Code", use_container_width=True):
                    code = coupon_input.strip().upper()
                    if code == "CARPET10":
                        st.session_state.applied_coupon = {"code": "CARPET10", "type": "pct", "val": 10}
                        st.success("10% Extra Discount applied!")
                        st.rerun()
                    elif code == "BHADOHI500":
                        st.session_state.applied_coupon = {"code": "BHADOHI500", "type": "flat", "val": 500}
                        st.success("₹500 Extra Discount applied!")
                        st.rerun()
                    else:
                        st.error("Invalid Promo Code")

            coupon_discount = 0
            if st.session_state.applied_coupon:
                coup = st.session_state.applied_coupon
                if coup["type"] == "pct":
                    coupon_discount = int(total_selling_price * (coup["val"] / 100))
                else:
                    coupon_discount = min(total_selling_price, coup["val"])
                st.info(f"✨ Coupon `{coup['code']}` applied: -₹{coupon_discount:,} savings!")

            final_total = max(0, total_selling_price - coupon_discount)
            product_discount_savings = max(0, total_mrp - total_selling_price)
            total_savings = product_discount_savings + coupon_discount

            # Flipkart/Amazon Style Price Details Card
            coupon_html = f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; color:#388e3c;'><span>Coupon Discount</span><span>- ₹{coupon_discount:,}</span></div>" if coupon_discount > 0 else ""
            price_details_html = (
                f"<div style='background:#ffffff; border:1px solid #e5e7eb; border-radius:10px; padding:18px; margin-top:15px;'>"
                f"<b style='color:#878787; font-size:13px; text-transform:uppercase; letter-spacing:0.5px;'>Price Details</b>"
                f"<hr style='margin:8px 0 12px 0; border:0; border-top:1px solid #f1f5f9;'>"
                f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px;'><span>Total MRP</span><span><del style='color:#878787;'>₹{total_mrp:,}</del></span></div>"
                f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; color:#388e3c;'><span>Product Discount</span><span>- ₹{product_discount_savings:,}</span></div>"
                f"{coupon_html}"
                f"<div style='display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px;'><span>Delivery Charges</span><span style='color:#388e3c;'><b>FREE</b> <del style='color:#878787; font-size:12px;'>₹199</del></span></div>"
                f"<hr style='margin:10px 0; border:0; border-top:1px dashed #cbd5e1;'>"
                f"<div style='display:flex; justify-content:space-between; font-size:18px; font-weight:800; color:#212121;'><span>Total Amount</span><span style='color:#2874f0;'>₹{final_total:,}</span></div>"
                f"<div style='margin-top:12px; background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; padding:8px 12px; border-radius:6px; font-size:13px; font-weight:700; text-align:center;'>🎉 You will save ₹{total_savings:,} on this order!</div>"
                f"</div>"
            )
            st.markdown(price_details_html, unsafe_allow_html=True)
            
        with col_summary:
            st.markdown("### 🚚 Delivery Details")
            with st.form("checkout_form"):
                customer_name = st.text_input("Full Name *", placeholder="e.g. Ramesh Maurya")
                phone = st.text_input("Mobile Number *", placeholder="10-digit mobile number")
                address = st.text_area(
                    "Delivery Address *",
                    placeholder="House/Plot No., Street, Landmark, City...",
                    height=90,
                )
                pincode = st.text_input("PIN Code *", max_chars=6, placeholder="6-digit Postal PIN")
                
                submit_order = st.form_submit_button("Proceed to Pay (UPI) 🚀", type="primary", use_container_width=True)
                if submit_order:
                    if not customer_name or not phone or not address or not pincode:
                        st.error("⚠️ Please fill in all mandatory fields!")
                    elif not phone.isdigit() or len(phone) != 10:
                        st.error("⚠️ Enter a valid 10-digit mobile number.")
                    elif not pincode.isdigit() or len(pincode) != 6:
                        st.error("⚠️ Enter a valid 6-digit postal PIN Code.")
                    else:
                        order_data = {
                            "customer_name": customer_name,
                            "phone": phone,
                            "address": address,
                            "home_address": f"Promo: {st.session_state.applied_coupon['code']}" if st.session_state.applied_coupon else "None",
                            "pincode": pincode,
                            "total_amount": int(final_total),
                            "payment_status": "Pending",
                        }
                        try:
                            with st.spinner("Creating your order securely..."):
                                time.sleep(1)
                                order_id = None
                                if supabase:
                                    res = supabase.table("orders").insert(order_data).execute()
                                    if res.data and len(res.data) > 0:
                                        order_id = res.data[0].get("id")
                                
                                st.session_state.order_ready = {
                                    "order_id": order_id if order_id else random.randint(1000, 9999),
                                    "name": customer_name,
                                    "amount": final_total,
                                    "phone": phone,
                                    "address": address,
                                    "pincode": pincode,
                                }
                                st.session_state.cart = {}
                                st.session_state.applied_coupon = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"Order placement error: {e}")

# ==============================================================================
# PAGE 4: ADMIN DASHBOARD
# ==============================================================================
elif st.session_state.page == "⚙️ Admin Panel":
    if not st.session_state.admin_logged_in:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0b0f19 !important;
                color: #38bdf8 !important;
            }
            .cyber-box {
                background: rgba(15, 23, 42, 0.9);
                border: 2px solid #38bdf8;
                box-shadow: 0 0 25px rgba(56, 189, 248, 0.25);
                border-radius: 14px;
                padding: 40px;
                max-width: 440px;
                margin: auto;
                text-align: center;
                margin-top: 40px;
            }
            .cyber-title {
                color: #f43f5e;
                font-family: 'Courier New', Courier, monospace;
                font-size: 26px;
                font-weight: 800;
                letter-spacing: 2px;
                margin-bottom: 20px;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='cyber-box'>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-title'>[ ADMIN MAINFRAME ]</div>", unsafe_allow_html=True)
        admin_user = st.text_input("USER ID", placeholder="Admin username")
        admin_pass = st.text_input("PASSWORD", type="password", placeholder="Password")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("AUTHENTICATE ACCESS ⚡", use_container_width=True, type="primary"):
            if admin_user and admin_pass:
                with st.spinner("Verifying credentials..."):
                    if supabase:
                        try:
                            response = (
                                supabase.table("admins")
                                .select("*")
                                .eq("username", admin_user)
                                .eq("password", admin_pass)
                                .execute()
                            )
                            if response.data and len(response.data) > 0:
                                st.session_state.admin_logged_in = True
                                st.success("ACCESS GRANTED.")
                                time.sleep(0.8)
                                st.rerun()
                            else:
                                st.error("ACCESS DENIED: Incorrect credentials.")
                        except Exception as e:
                            st.error(f"Auth database connection failed: {e}")
                    else:
                        if admin_user == "admin" and admin_pass == "admin123":
                            st.session_state.admin_logged_in = True
                            st.rerun()
                        else:
                            st.error("Invalid credentials (demo: admin / admin123)")
            else:
                st.warning("Please fill in both fields.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Admin Header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("## ⚙️ Executive Admin Dashboard")
            st.caption("Manage incoming orders, catalog items, and track revenue KPIs.")
        with col2:
            if st.button("Logout 🔴", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.markdown("---")

        tab_orders, tab_add, tab_catalog, tab_analytics = st.tabs([
            "📦 Manage Orders", "➕ Add Product", "🏷️ Edit Catalog", "📊 Sales Analytics"
        ])

        # TAB 1: ORDER MANAGEMENT
        with tab_orders:
            st.markdown("### Customer Orders & Status Dispatcher")
            if supabase:
                try:
                    orders_res = supabase.table("orders").select("*").order("id", desc=True).limit(50).execute()
                    orders_list = orders_res.data if orders_res.data else []
                except Exception as e:
                    st.error(f"Could not load orders: {e}")
                    orders_list = []
            else:
                orders_list = []

            if not orders_list:
                st.info("No customer orders recorded yet.")
            else:
                for ord in orders_list:
                    with st.expander(f"Order #{ord.get('id')} — {ord.get('customer_name')} | ₹{ord.get('total_amount', 0):,} | {ord.get('payment_status', 'Pending')}"):
                        o_col1, o_col2 = st.columns([2, 1.2])
                        with o_col1:
                            st.write(f"👤 **Customer:** {ord.get('customer_name')}")
                            st.write(f"📞 **Phone:** {ord.get('phone')}")
                            st.write(f"📍 **Address:** {ord.get('address')}, PIN: {ord.get('pincode')}")
                            st.write(f"💳 **Amount:** ₹{ord.get('total_amount', 0):,}")
                            st.write(f"ℹ️ **Notes / UTR Info:** {ord.get('home_address', 'None')}")
                            
                            c_phone = ord.get('phone', '')
                            wa_cust_link = f"https://wa.me/91{c_phone}?text=Hello%20{quote(str(ord.get('customer_name')))},%20update%20regarding%20your%20Carpet%20Order%20%23{ord.get('id')}:"
                            st.markdown(f"[💬 Message Customer on WhatsApp]({wa_cust_link})")

                        with o_col2:
                            current_stat = ord.get("payment_status", "Pending")
                            stat_options = ["Pending", "Paid / Confirmed", "Dispatched", "Delivered", "Cancelled"]
                            cur_index = stat_options.index(current_stat) if current_stat in stat_options else 0
                            
                            new_stat = st.selectbox(
                                "Update Status:", stat_options, index=cur_index, key=f"stat_sel_{ord.get('id')}"
                            )
                            if st.button("Save Status Update 💾", key=f"btn_stat_{ord.get('id')}", type="primary"):
                                if supabase:
                                    supabase.table("orders").update({"payment_status": new_stat}).eq("id", ord.get("id")).execute()
                                    st.success(f"Order #{ord.get('id')} updated to '{new_stat}'")
                                    st.rerun()

        # TAB 2: ADD NEW PRODUCT (WITH ORIGINAL MRP & DISCOUNT CALCULATOR)
        with tab_add:
            st.markdown("### ✨ Add New Rug to Catalog")
            with st.form("add_product_form", clear_on_submit=True):
                p_col1, p_col2, p_col3 = st.columns([2, 1, 1])
                with p_col1:
                    new_name = st.text_input("Carpet / Rug Title *", placeholder="e.g. Persian Medallion Hand-Knotted Silk Rug")
                with p_col2:
                    new_price = st.number_input("Selling Price (₹) *", min_value=100, step=100, value=2500, help="The final discounted price customers pay")
                with p_col3:
                    new_mrp = st.number_input("Original MRP (₹)", min_value=0, step=100, value=5000, help="Original price for strikethrough (e.g. ₹5,000 for 50% OFF)")
                
                img_col1, img_col2 = st.columns(2)
                with img_col1:
                    uploaded_img = st.file_uploader("Upload Image directly (JPG/PNG)", type=["jpg", "jpeg", "png", "webp"])
                with img_col2:
                    new_img_url = st.text_input("Or Paste Supabase / External Image URL", placeholder="https://...")
                
                new_desc = st.text_area("Product Description & Specs", placeholder="Knot count, weave type, dimensions (e.g. 5x8 ft), color palette...", height=100)
                
                submit_new_prod = st.form_submit_button("➕ Publish to Catalog", type="primary")
                if submit_new_prod:
                    if not new_name or not new_price:
                        st.warning("Please specify both product title and price.")
                    else:
                        final_img_path = new_img_url
                        if uploaded_img is not None and supabase:
                            try:
                                file_bytes = uploaded_img.read()
                                file_name = f"rug_{int(time.time())}_{uploaded_img.name}"
                                supabase.storage.from_("image").upload(file_name, file_bytes)
                                final_img_path = supabase.storage.from_("image").get_public_url(file_name)
                            except Exception as e:
                                st.error(f"Image storage upload warning: {e}")
                        
                        if not final_img_path:
                            final_img_path = "https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=600&q=80"

                        prod_payload = {
                            "name": new_name,
                            "price": int(new_price),
                            "description": new_desc,
                            "image_path": final_img_path,
                        }
                        if supabase:
                            try:
                                supabase.table("products").insert(prod_payload).execute()
                                st.success(f"✅ Successfully added **{new_name}** to the catalog!")
                                if "products" in st.session_state:
                                    del st.session_state.products
                                st.balloons()
                            except Exception as e:
                                st.error(f"Database error: {e}")
                        else:
                            st.success(f"Demo Mode: Added {new_name}!")

        # TAB 3: EDIT / DELETE PRODUCTS
        with tab_catalog:
            st.markdown("### 🏷️ Manage Catalog Items")
            if "products" in st.session_state and st.session_state.products:
                for p in st.session_state.products:
                    price, mrp, discount_pct, _ = get_pricing_details(p)
                    with st.expander(f"#{p.get('id')} {p.get('name')} — ₹{price:,} (MRP: ₹{mrp:,} | {discount_pct}% OFF)"):
                        e_c1, e_c2, e_c3 = st.columns([1.5, 3, 1])
                        with e_c1:
                            if p.get("image_path"):
                                st.image(p["image_path"], width=120)
                        with e_c2:
                            st.write(f"**Name:** {p.get('name')}")
                            st.write(f"**Description:** {p.get('description')}")
                            st.write(f"**Price:** ₹{price:,} | **MRP:** ₹{mrp:,} | **Discount:** {discount_pct}% OFF")
                        with e_c3:
                            if st.button("🗑️ Delete Rug", key=f"del_prod_{p.get('id')}"):
                                if supabase:
                                    try:
                                        supabase.table("products").delete().eq("id", p.get("id")).execute()
                                        st.success(f"Deleted product #{p.get('id')}")
                                        if "products" in st.session_state:
                                            del st.session_state.products
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Failed to delete: {e}")

        # TAB 4: SALES ANALYTICS & KPIS
        with tab_analytics:
            st.markdown("### 📊 Business Performance & Metrics")
            if supabase:
                try:
                    all_orders = supabase.table("orders").select("*").execute().data or []
                except Exception:
                    all_orders = []
            else:
                all_orders = [{"total_amount": 8500, "payment_status": "Dispatched"}]

            total_rev = sum(o.get("total_amount", 0) for o in all_orders)
            total_orders_count = len(all_orders)
            pending_count = sum(1 for o in all_orders if "Pending" in o.get("payment_status", "Pending"))
            avg_val = int(total_rev / total_orders_count) if total_orders_count > 0 else 0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Revenue", f"₹{total_rev:,}")
            m2.metric("Total Orders", f"{total_orders_count}")
            m3.metric("Pending Verification", f"{pending_count}")
            m4.metric("Avg Order Value", f"₹{avg_val:,}")

# ==============================================================================
# 8. PREMIUM TRUST FOOTER
# ==============================================================================
trusted_light_footer = """
<style>
.trust-footer {
    background-color: #ffffff;
    color: #475569;
    padding: 50px 35px 20px 35px;
    margin-top: 70px;
    border-top: 3px solid #2874f0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.03);
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
.tf-col { flex: 1; min-width: 220px; }
.tf-col h4 {
    color: #0f172a;
    margin-bottom: 16px;
    font-size: 17px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tf-col p { font-size: 13.5px; line-height: 1.7; color: #475569; }
.tf-col a {
    color: #64748b;
    text-decoration: none;
    font-size: 14px;
    line-height: 2.1;
    display: flex;
    align-items: center;
    transition: color 0.2s ease;
}
.tf-col a::before {
    content: '▸'; margin-right: 8px; color: #2874f0; font-size: 16px;
}
.tf-col a:hover { color: #2874f0; font-weight: 600; }
.trust-badges {
    margin-top: 15px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12.5px;
    font-weight: 700;
    color: #15803d;
    background: #f0fdf4;
    padding: 6px 10px;
    border-radius: 6px;
    border: 1px solid #bbf7d0;
}
.tf-bottom {
    text-align: left;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    margin-top: 35px;
    font-size: 12.5px;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
}
.tf-bottom b { color: #1e293b; }
.secure-payments img {
    height: 22px;
    margin-left: 12px;
    opacity: 0.8;
}
</style>
<div class="trust-footer">
    <div class="tf-container">
        <div class="tf-col">
            <h4>SM Carpet City</h4>
            <p>Direct from the master weavers of Bhadohi. Certified authentic, hand-knotted and hand-tufted heirloom rugs delivered with pride.</p>
            <div class="trust-badges">
                <div class="badge">🔒 100% Encrypted UPI Payments</div>
                <div class="badge">✅ Verified Bhadohi Artisan Quality</div>
            </div>
        </div>
        <div class="tf-col">
            <h4>Quick Navigation</h4>
            <a href="#">All Rugs & Carpets</a>
            <a href="#">Live Order Tracking</a>
            <a href="#">Custom Size Orders</a>
            <a href="#">Artisan Story</a>
        </div>
        <div class="tf-col">
            <h4>Policies & Care</h4>
            <a href="#">Carpet Cleaning & Care</a>
            <a href="#">Terms & Conditions</a>
            <a href="#">15-Day Return Policy</a>
            <a href="#">Insured Shipping Policy</a>
        </div>
        <div class="tf-col">
            <h4>Contact & Workshop</h4>
            <p>📍 Sector 11, Carpet City Nijampur,<br>Bhadohi, Uttar Pradesh - 221314</p>
            <p>📞 +91-8009076300</p>
            <p>✉️ support@smcarpetcity.com</p>
        </div>
    </div>
    <div class="tf-bottom">
        <span>© 2026-2027 <b>SM Carpet City</b>. All Rights Reserved.</span>
        <span class="secure-payments">
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/unified-payment-interface-upi-logo-png_seeklogo-333088.png" alt="UPI">
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/images.png" alt="Visa">
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/MasterCard_Logo.svg.webp" alt="Mastercard">
            <img src="https://fkesbvxhbudfbpjcqtez.supabase.co/storage/v1/object/public/image/RuPay.svg.webp" alt="RuPay">
        </span>
    </div>
</div>
"""
st.markdown(trusted_light_footer, unsafe_allow_html=True)
