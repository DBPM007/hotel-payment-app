import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Initialize Supabase client with caching
@st.cache_resource
def init_supabase():
    # Load from Streamlit secrets if deployed, else local .env
    if st.secrets:
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    else:
        load_dotenv("supa.env")
        return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

supabase = init_supabase()

# Page setup
st.set_page_config(layout="wide", page_title="Hotel Payment Manager")
page = st.sidebar.selectbox("Navigation", ["Data Entry", "Visualization"])

# --- Data Entry Page ---
if page == "Data Entry":
    st.title("🏠 Payment Data Entry")
    
    with st.form("payment_form", clear_on_submit=True):
        payment_id = str(uuid.uuid4())
        
        col1, col2 = st.columns(2)
        with col1:
            apartment_id = st.text_input("Apartment ID*", help="The apartment identifier")
            payment_type = st.selectbox(
                "Payment Type*", 
                ["DEWA", "Chiller", "VAT", "Brokerage", "Landlord", "Other"],
                index=0
            )
            category = st.selectbox(
                "Category*",
                ["Deposit", "Bill Payment", "Fee", "Rent", "Other"],
                index=1
            )
            amount = st.number_input("Amount (AED)*", min_value=0.0, step=0.01, format="%.2f")
            payment_date = st.date_input("Date*", datetime.now())
            
        with col2:
            frequency = st.selectbox(
                "Frequency*",
                ["One-time", "Monthly", "Quarterly", "Yearly"],
                index=1
            )
            payment_method = st.selectbox(
                "Payment Method*",
                ["Cash", "Cheque", "Bank Transfer", "Credit Card", "Other"],
                index=2
            )
            status = st.selectbox(
                "Status*",
                ["Pending", "Paid", "Overdue", "Failed", "Refunded"],
                index=1
            )
            reference_number = st.text_input("Reference Number", help="Transaction ID or receipt number")
            utility_account_id = st.text_input("Utility Account ID", help="DEWA/Chiller account number")
        
        submitted = st.form_submit_button("💾 Submit Payment")
        
        if submitted:
            if not apartment_id:
                st.error("Apartment ID is required!")
            else:
                try:
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
                    
                    response = supabase.table("payments").insert(data).execute()
                    if len(response.data) > 0:
                        st.success("Payment successfully recorded!")
                        st.balloons()
                    else:
                        st.error("Failed to save payment")
                except Exception as e:
                    st.error(f"Database error: {str(e)}")

# --- Visualization Page ---
elif page == "Visualization":
    st.title("📊 Payment Analytics")
    
    try:
        response = supabase.table("payments").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if df.empty:
            st.warning("No payment records found. Submit data first!")
        else:
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Payments", f"AED {df['amount'].sum():,.2f}")
            with col2:
                st.metric("Average Payment", f"AED {df['amount'].mean():,.2f}")
            with col3:
                st.metric("Total Records", len(df))
            
            st.divider()
            
            # Visualization 1: Payments by Type
            st.subheader("Payments by Category")
            type_totals = df.groupby('category')['amount'].sum().reset_index()
            st.bar_chart(type_totals, x='category', y='amount')
            
            # Visualization 2: Status Distribution
            st.subheader("Payment Status")
            status_counts = df['status'].value_counts()
            st.bar_chart(status_counts)
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")