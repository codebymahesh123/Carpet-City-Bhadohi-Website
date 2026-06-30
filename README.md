# 👑 SM Carpet City - Premium Rugs E-Commerce Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Supabase](https://img.shields.io/badge/Supabase-Database-green.svg)
![Status](https://img.shields.io/badge/Status-Live-success.svg)

A modern, fully functional E-Commerce and Catalog platform built entirely with **Python & Streamlit**. It features a dynamic shopping cart, a secure Admin Dashboard, real-time database integration via Supabase, and a mobile-optimized UPI payment gateway using Deep Linking.

---

## 🚀 Advanced Features Highlight

* **State Management:** Complex cart functionality and user flow managed entirely through Streamlit's `st.session_state` without page reloads.
* **Dynamic UPI Integration (Deep Linking):** Generates real-time dynamic QR codes for desktop users and utilizes **UPI Intent Links** (`intent://`) for seamless one-click payments on mobile devices (GPay, PhonePe, Paytm).
* **Secure Admin Panel:** Cyber-security themed admin authentication system. Allows admins to dynamically add products to the database directly from the frontend UI.
* **BaaS Integration:** Leverages **Supabase (PostgreSQL)** for robust backend storage. Features `products`, `orders`, and `admins` tables with Row Level Security (RLS) configurations.
* **Custom UI/UX Injection:** Bypassed default Streamlit UI limitations using advanced CSS injection (`unsafe_allow_html=True`) to create a Flipkart/Amazon-style clean interface, custom floating action buttons (WhatsApp), and professional toast notifications.

---

## 🛠️ Tech Stack

* **Frontend:** Python (Streamlit), Custom HTML/CSS
* **Backend / Database:** Supabase (PostgreSQL)
* **Payment Gateway:** UPI Deep Links & `qrcode` library
* **Deployment:** Streamlit Community Cloud

---

## 📂 Database Schema (Supabase)

The app relies on 3 primary tables:
1. `products`: `id`, `name`, `price`, `description`, `image_path`, `created_at`
2. `orders`: `id`, `customer_name`, `phone`, `address`, `pincode`, `total_amount`, `payment_status`
3. `admins`: `username`, `password` (For admin dashboard access)

---

## 💻 Local Development Setup

To run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/codebymahesh123/Carpet-City-Bhadohi-Website.git
cd The Carpet city
