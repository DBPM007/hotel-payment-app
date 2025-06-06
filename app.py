import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    return {
        "apartments": pd.read_csv("apartments.csv"),
        "owners": pd.read_csv("property_owners.csv"),
        "registrations": pd.read_csv("property_registrations.csv"),
        "brokers": pd.read_csv("brokers.csv"),
        "brokerage": pd.read_csv("brokerage.csv"),
        "cheques": pd.read_csv("cheques.csv"),
        "furnishings": pd.read_csv("apartment_furnishings.csv"),
        "attributes": pd.read_csv("apartment_attributes.csv"),
        "amenities": pd.read_csv("apartment_amenities.csv"),
        "guests": pd.read_csv("guests.csv"),
        "employees": pd.read_csv("employees.csv"),
        "payments": pd.read_csv("payments.csv"),
        "wps": pd.read_csv("wps.csv"),
        "rent": pd.read_csv("rent.csv")
    }

def main():
    st.set_page_config(layout="wide")
    st.title("🏨 Comprehensive Hotel & Property Management Dashboard")
    data = load_data()

    df_apartments = data["apartments"]
    df_rent = data["rent"]
    df_cheques = data["cheques"]
    df_employees = data["employees"]
    df_wps = data["wps"]
    df_amenities = data["amenities"]
    df_brokerage = data["brokerage"]
    df_brokers = data["brokers"]

    # Filters
    st.sidebar.header("Filters")
    building = st.sidebar.selectbox("Select Building", ["All"] + sorted(df_apartments["building_name"].unique()))
    status = st.sidebar.selectbox("Apartment Status", ["All", "Occupied", "Vacant", "Maintenance"])
    
    if building != "All":
        df_apartments = df_apartments[df_apartments["building_name"] == building]
    if status != "All":
        df_apartments = df_apartments[df_apartments["status"] == status]

    # KPI Section
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        occ_rate = len(df_apartments[df_apartments["status"] == "Occupied"]) / len(df_apartments)
        st.metric("Occupancy Rate", f"{occ_rate:.1%}")
    with col2:
        st.metric("Total Rent Revenue", f"AED {df_rent['amount'].sum():,.2f}")
    with col3:
        avg_rent = df_rent.groupby("apartment_id")["amount"].sum().mean()
        st.metric("Avg Rent per Unit", f"AED {avg_rent:,.2f}")
    with col4:
        st.metric("Pending Cheques", len(df_cheques[df_cheques["status"] == "Pending"]))

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Property Overview", "Financials", "Operations", "Predictive Analytics"])

    with tab1:
        st.subheader("🏢 Property Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Apartment Types**")
            fig = px.pie(df_apartments, names="status")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("**Occupancy by Building**")
            occ_status = df_apartments.groupby(["building_name", "status"]).size().reset_index(name="count")
            fig = px.bar(occ_status, x="building_name", y="count", color="status", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        st.write("**Top 5 Amenities**")
        top_amenities = df_amenities["amenity_name"].value_counts().nlargest(5)
        fig = px.bar(top_amenities, title="Most Common Amenities")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("💰 Financial Overview")
        col1, col2 = st.columns(2)
        with col1:
            df_rent["month"] = pd.to_datetime(df_rent["payment_date"]).dt.to_period("M").astype(str)
            monthly = df_rent.groupby("month")["amount"].sum().reset_index()
            fig = px.line(monthly, x="month", y="amount", markers=True, title="Monthly Rent Collection")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(df_cheques, names="status", title="Cheque Status")
            st.plotly_chart(fig, use_container_width=True)
        st.write("**Brokerage by Broker**")
        df_brokerage = df_brokerage.merge(df_brokers, on="broker_id")
        broker_total = df_brokerage.groupby("name")["amount"].sum().sort_values(ascending=False)
        fig = px.bar(broker_total, title="Brokerage Fees by Broker")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🔧 Operational Metrics")
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df_employees, names="designation", title="Employees by Designation")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            df_wps["month"] = pd.to_datetime(df_wps["payment_date"]).dt.to_period("M").astype(str)
            monthly_sal = df_wps.groupby("month")["amount"].sum().reset_index()
            fig = px.line(monthly_sal, x="month", y="amount", markers=True, title="Monthly Salaries")
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("🔮 Predictive Analytics")

        st.markdown("### 📈 1. Occupancy Forecasting (Next 6 Months)")

        df_occupancy = df_rent.copy()
        df_occupancy["month"] = pd.to_datetime(df_occupancy["payment_date"]).dt.to_period("M").astype(str)
        occupancy_series = df_occupancy.groupby("month")["apartment_id"].nunique().reset_index(name="occupied_apartments")

        if not occupancy_series.empty and len(occupancy_series) >= 6:
            import statsmodels.api as sm
            from pandas.tseries.offsets import MonthEnd

            occupancy_series["month"] = pd.to_datetime(occupancy_series["month"]) + MonthEnd(1)
            occupancy_series.set_index("month", inplace=True)

            model = sm.tsa.statespace.SARIMAX(
                occupancy_series["occupied_apartments"],
                order=(1, 1, 1),
                seasonal_order=(1, 1, 0, 12)
            )
            results = model.fit()

            forecast = results.get_forecast(steps=6)
            forecast_df = forecast.summary_frame()
            forecast_df["month"] = pd.date_range(start=occupancy_series.index[-1] + MonthEnd(1), periods=6, freq="M")

            fig = px.line(forecast_df, x="month", y="mean", title="Forecasted Occupied Apartments (SARIMA)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to build occupancy forecast.")

        st.markdown("### 🧹 Maintenance Alert System")

        df_furnishings = data.get("furnishings", pd.DataFrame())
        if not df_furnishings.empty:
            maintenance_df = df_furnishings.copy()
            from sklearn.ensemble import RandomForestClassifier

            maintenance_df["age_years"] = pd.to_datetime("today").year - pd.to_datetime(maintenance_df["purchase_date"]).dt.year
            maintenance_df["maintenance_flag"] = maintenance_df["condition"].apply(lambda x: 1 if x in ["Poor", "Fair"] else 0)

            features = maintenance_df[["age_years", "cost"]]
            target = maintenance_df["maintenance_flag"]

            clf = RandomForestClassifier()
            clf.fit(features, target)

            st.write("**Feature Importance for Maintenance Prediction**")
            for name, score in zip(features.columns, clf.feature_importances_):
                st.write(f"{name}: {score:.2f}")

            st.write("**Predict Maintenance Need**")
            age_input = st.slider("Furnishing Age (years)", 0, 20, 5)
            cost_input = st.number_input("Cost (AED)", min_value=0, value=5000)
            prediction = clf.predict([[age_input, cost_input]])[0]
            st.success("⚠️ Maintenance Needed" if prediction == 1 else "✅ No Immediate Maintenance")
        else:
            st.info("Furnishing data not available.")

        st.markdown("### 🧠 Guest Segmentation Engine")

        df_guests = data.get("guests", pd.DataFrame())
        if not df_guests.empty:
            segmentation_df = df_guests.copy()
            segmentation_df["stay_duration"] = (
                pd.to_datetime(segmentation_df["check_out"]) - pd.to_datetime(segmentation_df["check_in"])
            ).dt.days

            seg_features = segmentation_df[["stay_duration"]]
            from sklearn.cluster import DBSCAN
            from sklearn.preprocessing import StandardScaler

            scaler = StandardScaler()
            seg_scaled = scaler.fit_transform(seg_features)

            dbscan = DBSCAN(eps=0.5, min_samples=5)
            segmentation_df["segment"] = dbscan.fit_predict(seg_scaled)

            st.write("**Guest Segments Based on Stay Duration (DBSCAN)**")
            fig = px.histogram(segmentation_df, x="stay_duration", color="segment", nbins=20, title="Guest Segmentation with DBSCAN")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Guest data not available.")

        st.markdown("### 💰 3. Dynamic Rent Pricing Recommendation")

        df_features = df_apartments.copy()
        rent_avg = df_rent.groupby("apartment_id")["amount"].mean().reset_index()
        df_features = df_features.merge(rent_avg, on="apartment_id", how="left").dropna(subset=["amount"])

        feature_cols = ["size_sqft", "floor_number", "year_built"]
        from sklearn.linear_model import LinearRegression

        X = df_features[feature_cols]
        y = df_features["amount"]
        reg = LinearRegression()
        reg.fit(X, y)

        st.write("**Feature Coefficients**")
        for name, coef in zip(feature_cols, reg.coef_):
            st.write(f"{name}: {coef:.2f}")

        st.write("**Predict Rent for a New Apartment**")
        input_size = st.number_input("Size (sqft)", min_value=200, max_value=10000, value=1000)
        input_floor = st.number_input("Floor Number", min_value=0, max_value=100, value=5)
        input_year = st.number_input("Year Built", min_value=1980, max_value=2025, value=2015)

        pred_rent = reg.predict([[input_size, input_floor, input_year]])[0]
        st.success(f"Recommended Rent: AED {pred_rent:,.2f}")

if __name__ == "__main__":
    main()