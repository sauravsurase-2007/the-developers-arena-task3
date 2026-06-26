# ============================================================
# Sales Data Analysis Project
# Author: Your Name
# Description: Analyze sales data to find total sales,
#              best-selling products, and generate a report
# ============================================================

import pandas as pd
from datetime import datetime

# ============================================================
# STEP 1: LOAD DATA
# ============================================================

print("=" * 50)
print("       SALES DATA ANALYSIS REPORT")
print("=" * 50)

# Load the CSV file into a DataFrame
df = pd.read_csv('sales_data.csv')

print(f"\n✅ Data loaded successfully!")
print(f"   Shape: {df.shape[0]} rows x {df.shape[1]} columns")


# ============================================================
# STEP 2: EXPLORE DATA
# ============================================================

print("\n--- COLUMN NAMES ---")
print("  ", list(df.columns))

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- FIRST 5 ROWS ---")
print(df.head())


# ============================================================
# STEP 3: CLEAN DATA
# ============================================================

print("\n--- CLEANING DATA ---")

# Check for missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print(f"\n  Missing values found:\n{missing[missing > 0]}")
    df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median())
    df['Total_Sales'] = df['Quantity'] * df['Price']
else:
    print("  No missing values found!")

# Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"  Duplicates removed: {before - after}")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

print(f"  Data cleaned. Final shape: {df.shape}")


# ============================================================
# STEP 4: ANALYZE SALES — CALCULATE METRICS
# ============================================================

print("\n--- CALCULATING METRICS ---\n")

# METRIC 1: Total Revenue
total_revenue = df['Total_Sales'].sum()
print(f"  METRIC 1 - Total Revenue: Rs.{total_revenue:,.2f}")

# METRIC 2: Best-Selling Product (by revenue)
product_revenue = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
best_product = product_revenue.idxmax()
best_product_revenue = product_revenue.max()
print(f"\n  METRIC 2 - Best-Selling Product: {best_product}")
print(f"             Revenue: Rs.{best_product_revenue:,.2f}")

# METRIC 3: Top Region by Sales
region_sales = df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
top_region = region_sales.idxmax()
print(f"\n  METRIC 3 - Top Region by Sales: {top_region}")
print(f"             Revenue: Rs.{region_sales[top_region]:,.2f}")

# METRIC 4: Average Order Value
avg_order = df['Total_Sales'].mean()
print(f"\n  METRIC 4 - Average Order Value: Rs.{avg_order:,.2f}")

# METRIC 5: Total Units Sold
total_units = df['Quantity'].sum()
print(f"\n  METRIC 5 - Total Units Sold: {int(total_units)}")

# METRIC 6: Total Unique Customers
total_customers = df['Customer_ID'].nunique()
print(f"\n  METRIC 6 - Total Unique Customers: {total_customers}")


# ============================================================
# STEP 5: CREATE REPORT
# ============================================================

print("\n--- GENERATING REPORT ---\n")

report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

report = f"""# Sales Analysis Report
Generated on: {report_date}

## Summary
| Metric                  | Value                                        |
|-------------------------|----------------------------------------------|
| Total Revenue           | Rs.{total_revenue:,.2f}                      |
| Best-Selling Product    | {best_product} (Rs.{best_product_revenue:,.2f}) |
| Top Region              | {top_region} (Rs.{region_sales[top_region]:,.2f}) |
| Average Order Value     | Rs.{avg_order:,.2f}                          |
| Total Units Sold        | {int(total_units)}                           |
| Total Unique Customers  | {total_customers}                            |

## Revenue by Product
{product_revenue.to_string()}

## Revenue by Region
{region_sales.to_string()}

## Insights
- The highest-earning product is **{best_product}** contributing Rs.{best_product_revenue:,.2f} to total revenue.
- **{top_region}** region leads in sales performance.
- Average order size is Rs.{avg_order:,.2f}.
- A total of {total_customers} unique customers made purchases.
"""

# Save report to file
with open('analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("  Report saved to: analysis_report.md")
print("\n" + "=" * 50)
print("       ANALYSIS COMPLETE!")
print("=" * 50)
