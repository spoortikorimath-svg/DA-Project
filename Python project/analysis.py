"""
analysis.py
-----------
Pandas + NumPy analysis functions for cloud_infra_usage_cost.csv.

Run:  python analysis.py   -> prints a console report
Import into app.py for the Streamlit dashboard.
"""

import numpy as np
import pandas as pd

# Maps each Service to a cost category, so we can answer
# "compute vs storage vs network vs database" without a Provider column.
SERVICE_CATEGORY = {
    "Compute Instances": "Compute",
    "Serverless Functions": "Compute",
    "Managed Kubernetes": "Compute",
    "Object Storage": "Storage",
    "Block Storage": "Storage",
    "Managed Database": "Database",
    "Data Warehouse": "Database",
    "Content Delivery (CDN)": "Network",
    "Load Balancer": "Network",
    "Data Transfer / Egress": "Network",
}


def load_data(path: str = "cloud_infra_usage_cost.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Usage Date"])
    df["Category"] = df["Service"].map(SERVICE_CATEGORY).fillna("Other")
    return df


def total_cost(df: pd.DataFrame) -> float:
    return round(df["Cost"].sum(), 2)


def cost_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Category")["Cost"]
        .sum()
        .round(2)
        .reindex(["Compute", "Storage", "Database", "Network", "Other"])
        .dropna()
        .reset_index()
    )


def category_cost(df: pd.DataFrame, category: str) -> float:
    return round(df.loc[df["Category"] == category, "Cost"].sum(), 2)


def data_transfer_total_gb(df: pd.DataFrame) -> float:
    return round(df["Data Transfer GB"].sum(), 1)


def service_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Service")["Cost"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )


def region_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Region")["Cost"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )


def department_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Department")["Cost"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )


def environment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Environment")["Cost"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
    )


def monthly_cost(df: pd.DataFrame) -> pd.DataFrame:
    m = df.copy()
    m["Month"] = m["Usage Date"].dt.to_period("M").astype(str)
    return m.groupby("Month")["Cost"].sum().round(2).reset_index()


def top_accounts(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Account ID")["Cost"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


def detect_anomalies(df: pd.DataFrame, z_thresh: float = 2.5) -> pd.DataFrame:
    """NumPy z-score outlier detection within each Service (no ML)."""
    out = df.copy()
    out["z_score"] = out.groupby("Service")["Cost"].transform(
        lambda x: (x - np.mean(x)) / (np.std(x) if np.std(x) > 0 else 1)
    )
    anomalies = out[out["z_score"] > z_thresh].sort_values("z_score", ascending=False)
    cols = ["Usage Date", "Account ID", "Service", "Region", "Department", "Cost", "z_score"]
    return anomalies[cols]


if __name__ == "__main__":
    df = load_data()

    print("=" * 60)
    print(f"TOTAL CLOUD COST: ${total_cost(df):,.2f}")
    print("=" * 60)

    print("\n--- Cost by Category (Compute / Storage / Database / Network) ---")
    print(cost_by_category(df).to_string(index=False))

    print(f"\nTotal Data Transfer: {data_transfer_total_gb(df):,.1f} GB")

    print("\n--- Service Analysis ---")
    print(service_analysis(df).to_string(index=False))

    print("\n--- Region Analysis ---")
    print(region_analysis(df).to_string(index=False))

    print("\n--- Department Analysis ---")
    print(department_analysis(df).to_string(index=False))

    print("\n--- Monthly Cost ---")
    print(monthly_cost(df).to_string(index=False))

    print("\n--- Top 10 Accounts by Cost ---")
    print(top_accounts(df).to_string(index=False))

    print("\n--- Cost Anomalies (z-score > 2.5) ---")
    anomalies = detect_anomalies(df)
    print(anomalies.head(10).to_string(index=False) if len(anomalies) else "None found.")
