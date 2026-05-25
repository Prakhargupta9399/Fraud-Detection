
import pathlib
import pandas as pd
import streamlit as str
from turtle import st

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
    st. error(
        "CRITICAL ERROR: 'test_results.csv' could not be found. Please ensure it is placed in the same folder as 'app.py'."
    )
with st.sidebar:
    st.title("FraudOps")
    page       = st.radio("Navigate", ["Overview", "Transaction Explorer", "SHAP Explainer"])
    st.markdown("---")
    tier_sel   = st.selectbox("Risk Tier", ["All", "Critical", "Suspicious", "Clear"])
    hour_range = st.slider("Hour of Day", 0, 23, (0, 23))
    amt_max    = int(df["TransactionAmt"].max())
    amt_range  = st.slider("Transaction Amount ($)", 0, amt_max, (0, amt_max))

mask = (
    df["HourOfDay"].between(*hour_range) &
    df["TransactionAmt"].between(*amt_range)
)
if tier_sel != "All":
    mask &= df["RiskTier"] == tier_sel
filtered = df[mask]

# PAGE 1 — Overview
if page == "Overview":
    st.title("Fraud Operations Overview")
    total_txn      = len(filtered)
    total_fraud    = filtered["TrueLabel"].sum()
    detection_rate = filtered["TrueLabel"].mean() * 100 if total_txn > 0 else 0
    avg_fraud_amt  = filtered[filtered["TrueLabel"]==1]["TransactionAmt"].mean() if total_fraud > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transactions",  f"{total_txn:,}")
    c2.metric("Total Fraud Count",   f"{int(total_fraud):,}")
    c3.metric("Detection Rate",      f"{detection_rate:.2f}%")
    c4.metric("Avg Fraud Amount",    f"${avg_fraud_amt:.2f}")
    
    fig1 = px.histogram(filtered, x="HourOfDay", color="RiskTier", nbins=24,
                         title="Transaction Count by Hour of Day",
                         color_discrete_map={"Critical":"#e63946","Suspicious":"#f4a261","Clear":"#2a9d8f"})
    st.plotly_chart(fig1, use_container_width=True)
    
    tc   = filtered["RiskTier"].value_counts().reset_index()
    fig2 = px.pie(tc, names="RiskTier", values="count", hole=0.4,
                   title="Risk Tier Breakdown",
                   color="RiskTier",
                   color_discrete_map={"Critical":"#e63946","Suspicious":"#f4a261","Clear":"#2a9d8f"})
    st.plotly_chart(fig2, use_container_width=True)

# PAGE 2 — Transaction Explorer
elif page == "Transaction Explorer":
    st.title("Transaction Explorer")
    search = st.text_input("Search by TransactionID")
    if search:
        view = df[df["TransactionID"].astype(str).str.contains(search)]
    else:
        view = filtered
    st.dataframe(
        view[["TransactionID","TransactionAmt","HourOfDay",
              "RiskTier","FraudProb","TrueLabel"]].head(500),
        use_container_width=True
    )
    if search:
        row = df[df["TransactionID"].astype(str) == search]
        if not row.empty:
            st.markdown("#### Live Risk Score")
            prob = row["FraudProb"].values[0]
            tier = row["RiskTier"].values[0]
            icon = {"Critical":"🔴","Suspicious":"🟡","Clear":"🟢"}.get(tier,"")
            r1, r2, r3 = st.columns(3)
            r1.metric("Fraud Probability", f"{prob:.4f}")
            r2.metric("Risk Tier", f"{icon} {tier}")
            r3.metric("Amount", f"${row['TransactionAmt'].values[0]:.2f}")

# PAGE 3 — SHAP Explainer
elif page == "SHAP Explainer":
    st.title("SHAP Explainer")
    tid = st.text_input("Enter TransactionID")
    if tid:
        row = df[df["TransactionID"].astype(str) == tid]
        if row.empty:
            st.warning("TransactionID not found.")
        else:
            prob = row["FraudProb"].values[0]
            tier = row["RiskTier"].values[0]
            st.metric("Fraud Probability", f"{prob:.4f}")
            st.metric("Risk Tier", tier)
            skip      = ["TransactionID","FraudProb","TrueLabel","RiskTier"]
            feat_cols = [c for c in df.columns if c not in skip]
            X_row     = row[feat_cols].values
            explainer = shap.TreeExplainer(model)
            sv_row    = explainer.shap_values(X_row)
            if isinstance(sv_row, list): sv_row = sv_row[1]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            shap.waterfall_plot(
                shap.Explanation(values=sv_row[0],
                                 base_values=explainer.expected_value,
                                 data=X_row[0], feature_names=feat_cols),
                max_display=15, show=False)
            st.pyplot(fig)
            
            st.markdown("**Plain-English Explanation:**")
            top3 = np.argsort(np.abs(sv_row[0]))[::-1][:3]
            for i in top3:
                d = "increased" if sv_row[0][i] > 0 else "decreased"
                st.write(f"- `{feat_cols[i]}` {d} fraud risk by {abs(sv_row[0][i]):.4f} SHAP units.")
