# 🛡️ Fraud Detection - FraudOps Dashboard

An end-to-end Machine Learning web application deployed on Streamlit Cloud that monitors, evaluates, and flags fraudulent transactions in real-time.

---

## 🚀 Live Application

The operational application is fully deployed and accessible on the web:

### [👉 Click Here to Open the Live FraudOps Dashboard](https://blbcwb9fpesnqtvttdg8mc.streamlit.app/)

*Note: Replace the link above with your actual live Streamlit URL once deployment finishes.*

---

## 📁 Repository Structure

The project directory must be organized as follows for the automated deployment paths to function correctly:

```text
fraud-detection/
│
├── .github/                  # GitHub Actions (Optional)
├── dashboard/                # Main application folder
│   ├── app.py                # Streamlit UI execution script
│   ├── model.pkl             # Trained ML model artifact
│   └── test_results.csv      # Local evaluation dataset
│
├── README.md                 # Project documentation
└── requirements.txt          # Production dependencies
