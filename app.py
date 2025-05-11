import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv("supa.env")

# Initialize Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Page setup
st.set_page_config(layout="wide")
page = st.sidebar.selectbox("Navigation", ["Data Entry", "Visualization"])

if page == "Data Entry":
    st.title("🏠 Payment Data Entry")
    with st.form("payment_form"):
        payment_id = str(uuid.uuid4())
        
        col1, col2 = st.columns(2)
        with col1:
            apartment_id = st.text_input("Apartment ID*")
            payment_type = st.selectbox("Payment Type*", ["DEWA", "Chiller", "VAT", "Brokerage", "Landlord", "Other"])
            category = st.selectbox("Category*", ["Deposit", "Bill Payment", "Fee", "Rent", "Other"])
            amount = st.number_input("Amount*", min_value=0.0, step=0.01)
            payment_date = st.date_input("Date*", datetime.now())
            
        with col2:
            frequency = st.selectbox("Frequency*", ["One-time", "Monthly", "Quarterly", "Yearly"])
            payment_method = st.selectbox("Payment Method*", ["Cash", "Cheque", "Bank Transfer", "Credit Card", "Other"])
            status = st.selectbox("Status*", ["Pending", "Paid", "Overdue", "Failed", "Refunded"])
            reference_number = st.text_input("Reference Number")
            utility_account_id = st.text_input("Utility Account ID")
        
        submitted = st.form_submit_button("Submit Payment")
        
        if submitted and apartment_id:
            data = {
                "payment_id": payment_id,
                "apartment_id": apartment_id,
                "type": payment_type,
                "category": category,
                "amount": amount,
                "date": payment_date.strftime("%Y-%m-%d"),
                "frequency": frequency,
                "payment_method": payment_method,
                "status": status,
                "reference_number": reference_number,
                "utility_account_id": utility_account_id
            }
            
            # Insert into Supabase
            supabase.table("payments").insert(data).execute()
            st.success("Payment saved to Supabase!")
            st.balloons()

elif page == "Visualization":
    st.title("📊 Payment Analytics")
    # Fetch data from Supabase
    payments = supabase.table("payments").select("*").execute().data
    df = pd.DataFrame(payments)
    
    if df.empty:
        st.warning("No data yet. Submit payments first!")
    else:
        st.metric("Total Payments", f"${df['amount'].sum():,.2f}")
        # Add your Plotly charts here (same as before)