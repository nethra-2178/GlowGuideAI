import streamlit as st
from datetime import datetime
import sqlite3
import json

# -------------------- CUSTOM UI THEME --------------------
def apply_custom_theme():
    st.markdown(
        """
        <style>
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #fff5f7 0%, #fdf2e9 100%);
        }

        /* Sidebar/Header styling */
        [data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.1);
        }

        /* Chat Message Bubbles */
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }

        /* Assistant Message Styling (Pink/Gold) */
        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: #ffffff !important;
            border-left: 5px solid #D4AF37 !important; /* Gold Accent */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }

        /* User Message Styling (Soft Rose) */
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #FFB6C1 !important;
            color: #333 !important;
            border-right: 5px solid #D4AF37 !important; /* Gold Accent */
        }

        /* Input Box Styling */
        .stChatInputContainer {
            padding-bottom: 20px;
        }
        
        div[data-testid="stChatInput"] {
            border: 2px solid #D4AF37 !important;
            border-radius: 25px;
        }

        /* Headers and Text */
        h1, h2, h3 {
            color: #D4AF37 !important;
            font-family: 'Playfair Display', serif;
            text-align: center;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="🤍",
    layout="centered"
)

apply_custom_theme()

# Add a pretty header
st.markdown("## ✨ GlowGuide AI ✨")
st.markdown("<p style='text-align: center; color: #888;'>Your Personal Beauty & Skincare Assistant</p>", unsafe_allow_html=True)
st.divider()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="🤍",
    layout="centered"
)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_flow" not in st.session_state:
    st.session_state.current_flow = None

if "order_id" not in st.session_state:
    st.session_state.order_id = None

# -------------------- DISPLAY CHAT HISTORY --------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- USER INPUT --------------------
user_input = st.chat_input(
    "Hi, I'm GlowGuide AI! How can I assist you today? 😊"
)

# -------------------- KNOWLEDGE BASE --------------------
ESCALATION_KEYWORDS = [
    "talk to human",
    "human agent",
    "agent",
    "customer care",
    "complaint",
    "not happy",
    "bad service",
    "refund issue"
]

ORDERS = {
    "GG123": "Out for Delivery 🚚",
    "GG124": "Shipped 📦",
    "GG125": "Delivered ✅",
    "GG126": "Order Processing ⏳",
    "GG127": "Cancelled ❌"
}

FAQS = {
    "shipping time": "Orders are delivered within 3–5 business days depending on your location.",
    "international shipping": "Currently, we only ship within India.",
    "delivery charges": "Free delivery on orders above ₹499. A ₹50 fee applies otherwise.",
    "product return policy": "Returns are accepted within 7 days if the product is unused and unopened.",
    "refund timeline": "Refunds are processed within 5–7 business days after approval.",
    "order cancellation": "Orders can be cancelled within 24 hours of placing them.",
    "payment issues": "If your payment failed, please retry or use another payment method.",
    "product authenticity": "All products are 100% genuine and sourced directly from brands.",
    "contact details": "Reach us at support@glowguide.ai",
}

RETURN_REASONS_ALLOWED = [
    "damaged",
    "wrong product",
    "expired",
    "missing item",
    "leakage",
    "broken packaging",
    "allergic reaction",
    "incorrect shade",
    "defective pump",
    "seal broken"
]

RETURN_REASONS_ALLOWED = [
    "damaged",
    "wrong product",
    "expired",
    "missing item",
    "leakage",
    "broken packaging",
    "allergic reaction",
    "incorrect shade",
    "defective pump",
    "seal broken"
]

RETURN_TIMELINE = "Your refund will be processed within 2–3 business days."

PAYMENT_RESPONSES = {
    "cod": "Cash on Delivery is available for orders below ₹2000.",
    "upi": "We support UPI, cards, and net banking.",
    "failed": "If your payment failed, it will be auto-refunded in 3–5 days.",
}

# -------------------- HELPER FUNCTIONS --------------------
def check_escalation(text):
    if not text:
        return False
    text = text.lower()
    return any(keyword in text for keyword in ESCALATION_KEYWORDS)

def is_return_intent(text):
    keywords = ["return", "refund", "replace", "replacement"]
    return any(k in text.lower() for k in keywords)

def extract_order_id(text):
    text = text.upper()
    for word in text.split():
        if word.startswith("GG"):
            return word
    return None

def extract_return_reason(text):
    text = text.lower()
    for reason in RETURN_REASONS_ALLOWED:
        if reason in text:
            return reason
    return None

# -------------------- CORE CHAT LOGIC --------------------
import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GlowGuide AI",
    page_icon="🤍",
    layout="centered"
)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_flow" not in st.session_state:
    st.session_state.current_flow = None

if "order_id" not in st.session_state:
    st.session_state.order_id = None

# -------------------- KNOWLEDGE BASE --------------------
ESCALATION_KEYWORDS = [
    "talk to human", "human agent", "agent", "customer care", 
    "complaint", "not happy", "bad service", "refund issue"
]

ORDERS = {
    "GG123": "Out for Delivery 🚚",
    "GG124": "Shipped 📦",
    "GG125": "Delivered ✅",
    "GG126": "Order Processing ⏳",
    "GG127": "Cancelled ❌"
}

FAQS = {
    "shipping time": "We know you're excited to receive your goodies! ✨ Our standard delivery usually takes **3–5 business days** depending on where you are located.",
    "international shipping": "Currently, we only ship within India to ensure our products reach you in perfect condition. 🇮🇳 We hope to go global soon! 🌍",
    "delivery charges": "We offer **Free Delivery** on all orders above ₹499! For smaller orders, a tiny fee of ₹50 applies. 🚚",
    "product return policy": "We want you to love your products! 💖 If it's not the right fit, we accept returns within **7 days**, provided the item is unused and the seal is intact.",
    "refund timeline": "Once approved, your refund will bloom back into your account within **5–7 business days**. 🏦",
    "order cancellation": "Changed your mind? No worries at all! You can cancel your order within **24 hours** of placing it. ⏳",
    "payment issues": "Oh no! If your payment didn't go through, please try again or use a different method. We're here if the trouble persists! 💳",
    "product authenticity": "Rest assured, beautiful! 🤍 Every single product we stock is **100% genuine** and sourced directly from our trusted brand partners.",
    "contact details": "Want to send us some love or need extra help? Reach our sweet team at **support@glowguide.ai** 💌",
}

RETURN_REASONS_ALLOWED = [
    "damaged", "wrong product", "expired", "missing item", 
    "leakage", "broken packaging", "allergic reaction", 
    "incorrect shade", "defective pump", "seal broken"
]

RETURN_TIMELINE = "You’ll see the refund reflected in your account within **2–3 business days**. ✨"

PAYMENT_RESPONSES = {
    "cod": "Yes! We offer **Cash on Delivery** for all orders under ₹2000 to make things easy for you. 💵",
    "upi": "We love a smooth checkout! We support **UPI (Google Pay, PhonePe), Credit/Debit Cards, and Net Banking**. 💳",
    "failed": "Don't worry! If your payment failed but money was deducted, it will be automatically refunded to you in **3–5 business days**. 🏦",
    "general": "We want to make your shopping experience easy! We accept **UPI, all major Cards, and Cash on Delivery**. 🛍️"
}

# -------------------- HELPER FUNCTIONS --------------------
def check_escalation(text):
    return any(keyword in text.lower() for keyword in ESCALATION_KEYWORDS)

def is_return_intent(text):
    return any(k in text.lower() for k in ["return", "refund", "replace"])

def is_order_status_intent(text):
    return any(k in text.lower() for k in ["where is my order", "order status", "track"])

def is_payment_intent(text):
    return any(k in text.lower() for k in ["pay", "payment", "cod", "upi", "price", "cost"])

def extract_order_id(text):
    text = text.upper()
    for oid in ORDERS.keys():
        if oid in text: return oid
    return None

def extract_return_reason(text):
    text = text.lower()
    for reason in RETURN_REASONS_ALLOWED:
        if reason in text: return reason
    return None

# -------------------- DISPLAY CHAT HISTORY --------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- CORE CHAT LOGIC --------------------

if user_input:
    # 1. Save and Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    user_query = user_input.lower()
    bot_response = ""

    # 2. LOGIC CHAIN
    
    # A. Human Escalation
    if check_escalation(user_query):
        bot_response = (
            "I'm so sorry things aren't going perfectly! 🤍\n\n"
            "I am connecting you with one of our **human support experts** right now. "
            "They will personally look into this for you within **2–4 hours**. 💬✨\n\n"
            "Is there anything else I can hold for you in the meantime?"
        )
        st.session_state.current_flow = None

    # B. Return Reason Flow
    elif st.session_state.current_flow == "return_reason":
        reason = extract_return_reason(user_query)
        if reason:
            bot_response = (
                f"Thank you for letting me know. 😊\n\n"
                f"I've successfully registered your return for **{reason}** (Order ID: {st.session_state.order_id}). "
                f"{RETURN_TIMELINE}\n\n"
                "We’ll send you an update via SMS as soon as it's processed! 🌸"
            )
            st.session_state.current_flow = None
            st.session_state.order_id = None
        else:
            bot_response = "I want to make sure we get this right! Could you please pick a reason like **Damaged, Leakage, or Wrong Product**? 🤍"

    # C. Return Order ID Flow
    elif st.session_state.current_flow == "return_order_id":
        oid = extract_order_id(user_query)
        if oid:
            st.session_state.order_id = oid
            bot_response = (
                f"I've found your order **{oid}**! 👍\n\n"
                "To help our team process this, could you tell me why you'd like to return it? "
                "(e.g., Was it damaged, a wrong product, or perhaps a leakage?)"
            )
            st.session_state.current_flow = "return_reason"
        else:
            bot_response = "I couldn't find that Order ID in our system. 🤍 Could you please double-check your confirmation email and try again? (Example: GG123)"

    # D. Order Status Flow
    elif st.session_state.current_flow == "order_status":
        oid = extract_order_id(user_query)
        if oid:
            bot_response = (
                f"Great news! ✨\n\n"
                f"The status for your order **{oid}** is: **{ORDERS[oid]}**.\n\n"
                "We're doing our best to get your glow to you as fast as possible! Anything else? 😊"
            )
            st.session_state.current_flow = None
        else:
            bot_response = "I'd love to check that for you! Could you please share a valid **Order ID**? It usually starts with 'GG' followed by three numbers. 📦"

    # E. Payment Query Flow
    elif st.session_state.current_flow == "payment_query":
        if "cod" in user_query: 
            bot_response = PAYMENT_RESPONSES["cod"]
        elif "upi" in user_query or "card" in user_query: 
            bot_response = PAYMENT_RESPONSES["upi"]
        else: 
            bot_response = PAYMENT_RESPONSES["general"]
        st.session_state.current_flow = None

    # F. New Intents
    elif is_return_intent(user_query):
        bot_response = "I'm sorry your order wasn't quite what you expected! 🤍 I can definitely help you start a return. Could you please share your **Order ID**? 📦"
        st.session_state.current_flow = "return_order_id"

    elif is_order_status_intent(user_query):
        bot_response = "Of course! Let's see where your package is. 🚚 Could you please share your **Order ID** (for example: GG123)?"
        st.session_state.current_flow = "order_status"

    elif is_payment_intent(user_query):
        if "cod" in user_query:
            bot_response = PAYMENT_RESPONSES["cod"]
        else:
            bot_response = "We want to make your shopping experience as smooth as silk! ✨ We accept **UPI, Cards, and COD**. Which one would you like more details on?"
            st.session_state.current_flow = "payment_query"

    # G. FAQ Check
    else:
        faq_found = False
        for question_key in FAQS.keys():
            if question_key in user_query:
                bot_response = FAQS[question_key]
                faq_found = True
                break 
        
        if not faq_found:
            bot_response = (
                "I'm here to make your GlowGuide experience wonderful! 🤍\n\n"
                "I didn't quite catch that, but I can help with **order tracking, returns, and payment questions**. "
                "What's on your mind? 😊"
            )

    # 3. Final Display & Save
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
