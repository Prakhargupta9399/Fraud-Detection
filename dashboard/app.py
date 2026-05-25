import pathlib
import pandas as pd
import streamlit as st  # <-- Fixed the import here!


# 1. Securely load the data without path errors
@st.cache_data
def load_data():
    # Finds the absolute path of the folder where app.py lives
    current_dir = pathlib.Path(__file__).parent.resolve()

    # Targets the test_results.csv file inside that same folder
    csv_path = current_dir / "test_results.csv"

    # Reads the CSV
    return pd.read_csv(csv_path)


# 2. App Layout and Logic
st.title("🛡️ Fraud Detection Dashboard")

try:
    # Call the load data function
    df = load_data()

    # Quick preview of the data to ensure it works
    st.success("Data loaded successfully!")
    st.write("### Data Preview", df.head())

# Friendly error fallback just in case the CSV is missing entirely
except FileNotFoundError:
    st.error(
        "CRITICAL ERROR: 'test_results.csv' could not be found. Please ensure it is placed in the same folder as 'app.py'."
    )
