import os
import pathlib
import pandas as pd
import streamlit as st

# 1. Setup the UI layout first
st.title("🛡️ Fraud Detection Dashboard")

# 2. Securely load the data with path debugging built-in
@st.cache_data
def load_data():
    current_dir = pathlib.Path(__file__).parent.resolve()
    csv_path = current_dir / "test_results.csv"

    # --- DEBUGGING INFORMATION ---
    st.write("### 🔍 Path Debugger")
    st.write(f"**Python is looking in this folder:** `{current_dir}`")
    st.write(f"**Expected full path to CSV file:** `{csv_path}`")

    # Check if the directory exists and list its files
    if current_dir.exists():
        st.write("**Actual files found in this folder:**", os.listdir(current_dir))
    else:
        st.write(" Directory does not exist!")
    st.write("---")
   

    return pd.read_csv(csv_path)


# 3. Execution Block
try:
    df = load_data()
    st.success("🎉 Data loaded successfully!")
    st.write("### Data Preview", df.head())

except FileNotFoundError:
    st.error(
        "CRITICAL ERROR: 'test_results.csv' could not be found. Look at the Path Debugger above to see what is missing."
    )
except Exception as e:
    st.error(f" An unexpected error occurred: {e}")
