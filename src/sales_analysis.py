import pandas as pd
import numpy as np


# ============================================================
# SUPERMARKET SALES ANALYSIS
# STEP 1: LOAD AND INSPECT DATA
# ============================================================

# Load dataset
df = pd.read_csv("data/supermarket_sales.csv")


# ------------------------------------------------------------
# Display basic information
# ------------------------------------------------------------

print("=" * 60)
print("SUPERMARKET SALES ANALYSIS")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())


# Dataset shape
print("\nDataset Shape:")
print(df.shape)


# Column names
print("\nColumn Names:")
print(df.columns.tolist())


# Data types and non-null values
print("\nDataset Information:")
df.info()


# Statistical summary
print("\nStatistical Summary:")
print(df.describe())


# Missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# BASIC SALES INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("BASIC SALES INFORMATION")
print("=" * 60)


total_sales = df["Sales"].sum()

total_transactions = len(df)

total_quantity = df["Quantity"].sum()

average_sales = df["Sales"].mean()

average_rating = df["Rating"].mean()


print(f"Total Sales        : ₹{total_sales:,.2f}")
print(f"Total Transactions : {total_transactions}")
print(f"Total Quantity     : {total_quantity}")
print(f"Average Sale       : ₹{average_sales:,.2f}")
print(f"Average Rating     : {average_rating:.2f}")


# ============================================================
# UNIQUE VALUES
# ============================================================

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

print("\nProducts:")
print(df["Product"].unique())

print("\nCategories:")
print(df["Category"].unique())

print("\nBranches:")
print(df["Branch"].unique())

print("\nCities:")
print(df["City"].unique())

print("\nCustomer Types:")
print(df["Customer Type"].unique())

print("\nPayment Methods:")
print(df["Payment Method"].unique())


print("\n" + "=" * 60)
print("INITIAL DATA ANALYSIS COMPLETE")
print("=" * 60)

# ============================================================
# PRODUCT SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT SALES ANALYSIS")
print("=" * 60)


# Total sales by product
product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


print("\nSales by Product:")
print(product_sales)


# Best-selling product by revenue
best_product = product_sales.idxmax()

best_product_sales = product_sales.max()


print("\nHighest Sales Product:")
print(f"Product : {best_product}")
print(f"Sales   : ₹{best_product_sales:,.2f}")

# ============================================================
# CATEGORY SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CATEGORY SALES ANALYSIS")
print("=" * 60)


# Total sales by category
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


print("\nSales by Category:")
print(category_sales)


# Highest-selling category
best_category = category_sales.idxmax()

best_category_sales = category_sales.max()


print("\nHighest Sales Category:")
print(f"Category : {best_category}")
print(f"Sales    : ₹{best_category_sales:,.2f}")

# ============================================================
# BRANCH SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("BRANCH SALES ANALYSIS")
print("=" * 60)


# Total sales by branch
branch_sales = (
    df.groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


print("\nSales by Branch:")
print(branch_sales)


# Highest-performing branch
best_branch = branch_sales.idxmax()

best_branch_sales = branch_sales.max()


# Get city of best branch
best_branch_city = (
    df.loc[
        df["Branch"] == best_branch,
        "City"
    ]
    .iloc[0]
)


print("\nBest Performing Branch:")
print(f"Branch : {best_branch}")
print(f"City   : {best_branch_city}")
print(f"Sales  : ₹{best_branch_sales:,.2f}")

# ============================================================
# PAYMENT METHOD ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PAYMENT METHOD ANALYSIS")
print("=" * 60)


# Count transactions by payment method
payment_counts = (
    df["Payment Method"]
    .value_counts()
)


print("\nTransactions by Payment Method:")
print(payment_counts)


# Most popular payment method
popular_payment = payment_counts.idxmax()

popular_payment_count = payment_counts.max()


print("\nMost Popular Payment Method:")
print(f"Payment Method : {popular_payment}")
print(f"Transactions   : {popular_payment_count}")

# ============================================================
# CUSTOMER TYPE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER TYPE ANALYSIS")
print("=" * 60)

# Calculate average sales for each customer type
customer_type_sales = (
    df.groupby("Customer Type")["Sales"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Sales by Customer Type:")
print(customer_type_sales)

# Get individual averages
member_average = df.loc[
    df["Customer Type"] == "Member", "Sales"
].mean()

normal_average = df.loc[
    df["Customer Type"] == "Normal", "Sales"
].mean()

print("\nCustomer Type Comparison:")
print(f"Member Average : ₹{member_average:,.2f}")
print(f"Normal Average : ₹{normal_average:,.2f}")

if member_average > normal_average:
    print("Higher Average Spending : Member")
else:
    print("Higher Average Spending : Normal")
    
    # ============================================================
# RATING ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("RATING ANALYSIS")
print("=" * 60)

# Average customer rating
average_rating = df["Rating"].mean()

print("\nAverage Customer Rating:")
print(f"Rating : {average_rating:.2f} / 5")

# Count each rating
rating_counts = (
    df["Rating"]
    .value_counts()
    .sort_index()
)

print("\nRating Distribution:")
print(rating_counts)