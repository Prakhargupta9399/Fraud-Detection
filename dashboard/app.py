import os
import pathlib
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    current_dir = pathlib.Path(__file__).parent.resolve()
    csv_path = current_dir / "test_results.csv"

    # --- DEBUGGING BLOCK ---
    st.write(f"**Current directory Python is looking in:** `{current_dir}`")
    st.write(f"**Expected full path to CSV:** `{csv_path}`")

    # List all files actually present in that folder
    if current_dir.exists():
        st.write("**Files found in this folder:**", os.listdir(current_dir))
    else:
        st.write(" Directory does not exist!")
    # -----------------------

    return pd.read_csv(csv_path)
