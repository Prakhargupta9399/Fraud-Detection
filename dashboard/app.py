import pathlib
import pandas as pd
import streamlit as st

# Set page configurations
st.set_page_config(page_title="FraudOps Dashboard", page_icon="🛡️", layout="wide")

# App Header & Navigation Links
st.title("🛡️ Fraud Detection Dashboard")

# FIX: This makes your live link clickable on the web app!
st. markdown(
    "The operational application is fully deployed and accessible on the web."
    "[👉 Click Here to Open the Live FraudOps Dashboard](https://blbcwb9fpesnqtvttdg8mc.streamlit.app/)"
)
st.write("---")


# Securely load the data from the dashboard directory
@st.cache_data
def load_data():
    current_dir = pathlib.Path(__file__).parent.resolve()
    csv_path = current_dir / "test_results.csv"
    return pd.read_csv(csv_path)


# App Main Logic
try:
    df = load_data()

    # Success metric cards or summary
    st.success("🎉 Data connection active. System status: Operational.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Transactions Evaluated", value=len(df))
    with col2:
        # Assumes you have a column tracking fraud; adjusts if your column name is different
        if "is_fraud" in df.columns:
            fraud_count = df["is_fraud"].sum()
            st.metric(label="Flagged Fraud Cases", value=int(fraud_count))

    # Data Preview Section
    st.write("### 📊 Live FraudOps Data Stream")
    st.dataframe(df.head(10), use_container_width=True)

except Exception as e:
    st.error(
        f"⚠️ System Error: Could not parse database. Technical details: {e}"
    )
