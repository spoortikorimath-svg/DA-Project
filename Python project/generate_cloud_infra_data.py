"""
generate_cloud_infra_data.py
-----------------------------
Generates a dataset matching this schema:
Account ID, Service, Region, Instance Type, Usage Date, Usage Hours,
Storage GB, Data Transfer GB, Cost, Environment, Department

Run:  python generate_cloud_infra_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(7)

# ---------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------
NUM_DAYS = 365
start_date = datetime.today() - timedelta(days=NUM_DAYS)
dates = [start_date + timedelta(days=i) for i in range(NUM_DAYS)]

accounts = [f"ACC-{1000+i}" for i in range(1, 16)]  # 15 accounts

# Service catalog with a category (used to derive Compute/Storage/Network cost)
# and typical instance types (blank for non-compute services).
services = {
    "Compute Instances":     {"category": "Compute", "instance_types": ["t3.micro", "t3.medium", "m5.large", "m5.xlarge", "c5.large", "r5.large"]},
    "Serverless Functions":  {"category": "Compute", "instance_types": ["N/A"]},
    "Managed Kubernetes":    {"category": "Compute", "instance_types": ["m5.large", "m5.xlarge", "c5.2xlarge"]},
    "Object Storage":        {"category": "Storage", "instance_types": ["N/A"]},
    "Block Storage":         {"category": "Storage", "instance_types": ["gp3", "io2", "st1"]},
    "Managed Database":      {"category": "Database", "instance_types": ["db.t3.medium", "db.m5.large", "db.r5.large"]},
    "Data Warehouse":        {"category": "Database", "instance_types": ["dw.large", "dw.xlarge"]},
    "Content Delivery (CDN)":{"category": "Network", "instance_types": ["N/A"]},
    "Load Balancer":         {"category": "Network", "instance_types": ["N/A"]},
    "Data Transfer / Egress":{"category": "Network", "instance_types": ["N/A"]},
}

regions = ["us-east-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-south-1", "ap-southeast-1"]
departments = ["Engineering", "Data Science", "Marketing", "Sales", "Finance", "IT Operations"]
environments = ["Production", "Staging", "Development"]

# Approximate unit rates (illustrative, not any real provider's actual pricing)
compute_hourly_rate = {"t3.micro": 0.0104, "t3.medium": 0.0416, "m5.large": 0.096,
                        "m5.xlarge": 0.192, "c5.large": 0.085, "r5.large": 0.126,
                        "c5.2xlarge": 0.34, "N/A": 0.05}
storage_gb_rate = {"gp3": 0.08, "io2": 0.125, "st1": 0.045, "N/A": 0.023}
db_hourly_rate = {"db.t3.medium": 0.068, "db.m5.large": 0.171, "db.r5.large": 0.24,
                   "dw.large": 0.50, "dw.xlarge": 1.00, "N/A": 0.10}
network_gb_rate = 0.09  # per GB data transfer

# Each account is consistently tied to one department + a "home" region,
# with a bit of cross-region usage — mirrors how real orgs are set up.
account_department = {acc: np.random.choice(departments, p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10]) for acc in accounts}
account_home_region = {acc: np.random.choice(regions) for acc in accounts}

# ---------------------------------------------------------------------
# Generate rows
# ---------------------------------------------------------------------
rows = []
for date in dates:
    weekday_factor = 1.0 if date.weekday() < 5 else 0.55
    # not every account has activity every day (skips dev/staging on some days)
    active_accounts = np.random.choice(accounts, size=np.random.randint(8, len(accounts) + 1), replace=False)

    for account in active_accounts:
        dept = account_department[account]
        home_region = account_home_region[account]
        # 85% of usage stays in the home region, 15% spills into another
        region = home_region if np.random.rand() < 0.85 else np.random.choice(regions)
        environment = np.random.choice(environments, p=[0.55, 0.25, 0.20])

        # each active account uses 1-3 services that day
        for service_name in np.random.choice(list(services.keys()),
                                               size=np.random.randint(1, 4), replace=False):
            meta = services[service_name]
            category = meta["category"]
            instance_type = np.random.choice(meta["instance_types"])

            usage_hours = 0.0
            storage_gb = 0.0
            transfer_gb = 0.0
            cost = 0.0

            if category == "Compute":
                usage_hours = round(np.random.gamma(shape=5, scale=3) * weekday_factor, 2)
                cost += usage_hours * compute_hourly_rate.get(instance_type, 0.05)
            elif category == "Storage":
                storage_gb = round(np.random.gamma(shape=8, scale=25), 1)
                cost += storage_gb * storage_gb_rate.get(instance_type, 0.023)
            elif category == "Database":
                usage_hours = round(np.random.gamma(shape=6, scale=4) * weekday_factor, 2)
                storage_gb = round(np.random.gamma(shape=4, scale=15), 1)
                cost += usage_hours * db_hourly_rate.get(instance_type, 0.1)
                cost += storage_gb * 0.10
            elif category == "Network":
                transfer_gb = round(np.random.gamma(shape=3, scale=10), 1)
                cost += transfer_gb * network_gb_rate

            # small noise + occasional spike (misconfigured autoscaling, forgotten resources)
            cost *= np.random.normal(1.0, 0.07)
            if np.random.rand() < 0.012:
                cost *= np.random.uniform(3, 6)
            cost = round(max(cost, 0.01), 2)

            rows.append({
                "Account ID": account,
                "Service": service_name,
                "Region": region,
                "Instance Type": instance_type,
                "Usage Date": date.date(),
                "Usage Hours": usage_hours,
                "Storage GB": storage_gb,
                "Data Transfer GB": transfer_gb,
                "Cost": cost,
                "Environment": environment,
                "Department": dept,
            })

df = pd.DataFrame(rows)
df = df.sort_values("Usage Date").reset_index(drop=True)

output_path = "cloud_infra_usage_cost.csv"
df.to_csv(output_path, index=False)

print(f"Generated {len(df):,} rows across {NUM_DAYS} days, {len(accounts)} accounts, {len(services)} services.")
print(f"Total cost: ${df['Cost'].sum():,.2f}")
print(f"Saved to {output_path}")
print(df.head())
