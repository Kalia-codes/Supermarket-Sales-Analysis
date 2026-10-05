import random
from decimal import Decimal
from pathlib import Path

import pandas as pd


# ============================================================
# SUPERMARKET SALES DATASET
# Based on the requirements/results in the project PDF
# ============================================================

random.seed(42)

NUM_ROWS = 500

# Required values from the project
CHEESE_TOTAL = Decimal("27906.30")
BEVERAGES_TOTAL = Decimal("56108.24")
BRANCH_C_TOTAL = Decimal("72469.45")

MEMBER_TOTAL = Decimal("144942.00")   # 300 × ₹483.14
NORMAL_TOTAL = Decimal("99414.00")    # 200 × ₹497.07

UPI_COUNT = 127
AVERAGE_RATING = Decimal("3.99")


# ============================================================
# PROJECT DATA
# ============================================================

branch_city = {
    "A": "Bangalore",
    "B": "Delhi",
    "C": "Mumbai"
}

payment_methods = [
    "UPI",
    "Cash",
    "Credit Card",
    "Debit Card"
]

products = {
    "Cheese": "Dairy",

    "Coffee": "Beverages",
    "Tea": "Beverages",
    "Juice": "Beverages",
    "Soft Drink": "Beverages",

    "Chips": "Snacks",
    "Chocolate": "Snacks",

    "Rice": "Groceries",
    "Pasta": "Groceries",
    "Noodles": "Groceries",

    "Soap": "Personal Care",
    "Shampoo": "Personal Care",
    "Toothpaste": "Personal Care",

    "Bread": "Bakery",
    "Cake": "Bakery",
    "Biscuits": "Bakery"
}


# ============================================================
# HELPER FUNCTION
# ============================================================

def distribute_total(total, count):
    """
    Distribute an exact total across 'count' rows.
    Returns values with exactly two decimal places.
    """

    total_cents = int(total * 100)

    # Generate random positive weights
    weights = [
        random.randint(50, 500)
        for _ in range(count)
    ]

    weight_sum = sum(weights)

    values = []

    allocated = 0

    for i in range(count - 1):

        cents = (
            total_cents * weights[i]
        ) // weight_sum

        # Make sure every row has positive sales
        cents = max(cents, 1)

        values.append(
            Decimal(cents) / Decimal("100")
        )

        allocated += cents

    # Last row gets exact remaining amount
    remaining = total_cents - allocated

    if remaining <= 0:
        raise ValueError("Invalid distribution")

    values.append(
        Decimal(remaining) / Decimal("100")
    )

    return values


# ============================================================
# GROUP DESIGN
# ============================================================

# Each tuple:
# (group name, number of rows, total sales,
#  number of member rows, member sales)

groups = [

    # Cheese
    (
        "CHEESE",
        60,
        CHEESE_TOTAL,
        36,
        Decimal("16500.00")
    ),

    # Beverages
    (
        "BEVERAGES",
        120,
        BEVERAGES_TOTAL,
        72,
        Decimal("33000.00")
    ),

    # Branch C sales
    (
        "BRANCH_C",
        120,
        BRANCH_C_TOTAL,
        72,
        Decimal("43000.00")
    ),

    # Remaining transactions
    (
        "OTHER",
        200,
        Decimal("87872.01"),
        120,
        Decimal("52442.00")
    )
]


rows = []

transaction_id = 1


# ============================================================
# CREATE GROUPS
# ============================================================

for group_name, row_count, group_total, member_count, member_total in groups:

    normal_count = row_count - member_count

    normal_total = group_total - member_total

    # Sales for Member customers
    member_sales = distribute_total(
        member_total,
        member_count
    )

    # Sales for Normal customers
    normal_sales = distribute_total(
        normal_total,
        normal_count
    )

    group_rows = []

    # --------------------------------------------------------
    # Member rows
    # --------------------------------------------------------

    for sales in member_sales:

        group_rows.append({
            "Customer Type": "Member",
            "Sales": sales
        })

    # --------------------------------------------------------
    # Normal rows
    # --------------------------------------------------------

    for sales in normal_sales:

        group_rows.append({
            "Customer Type": "Normal",
            "Sales": sales
        })


    # Shuffle customers inside group
    random.shuffle(group_rows)


    # --------------------------------------------------------
    # Create transactions
    # --------------------------------------------------------

    for item in group_rows:

        sales = item["Sales"]

        customer_type = item["Customer Type"]


        # ----------------------------------------------
        # Product
        # ----------------------------------------------

        if group_name == "CHEESE":

            product = "Cheese"

            branch = random.choice(["A", "B"])

        elif group_name == "BEVERAGES":

            product = random.choice([
                "Coffee",
                "Tea",
                "Juice",
                "Soft Drink"
            ])

            # Beverages are not placed in Branch C
            branch = random.choice(["A", "B"])

        elif group_name == "BRANCH_C":

            # Branch C group contains only non-beverage
            # and non-cheese products.

            product = random.choice([
                "Chips",
                "Chocolate",
                "Rice",
                "Pasta",
                "Noodles",
                "Soap",
                "Shampoo",
                "Toothpaste"
            ])

            branch = "C"

        else:

            product = random.choice([
                "Chips",
                "Chocolate",
                "Rice",
                "Pasta",
                "Noodles",
                "Soap",
                "Shampoo",
                "Toothpaste",
                "Bread",
                "Cake",
                "Biscuits"
            ])

            # Keep the remaining sales below Branch C
            branch = "A" if transaction_id % 2 == 0 else "B"


        category = products[product]

        city = branch_city[branch]


        # ----------------------------------------------
        # Quantity
        # ----------------------------------------------

        quantity = random.randint(1, 5)


        # ----------------------------------------------
        # Unit Price
        # ----------------------------------------------

        # We use quantity = 1 for some rows when necessary,
        # so Sales = Quantity × Unit Price remains exact.

        if transaction_id % 3 == 0:

            quantity = 1
            unit_price = sales

        else:

            # Keep sales relationship exact by choosing
            # quantity 1.
            quantity = 1
            unit_price = sales


        # ----------------------------------------------
        # Payment Method
        # ----------------------------------------------

        payment_method = random.choice(payment_methods)


        # ----------------------------------------------
        # Rating
        # ----------------------------------------------

        rating = Decimal("4.0")


        rows.append({

            "Transaction ID": transaction_id,

            "Product": product,

            "Category": category,

            "Branch": branch,

            "City": city,

            "Customer Type": customer_type,

            "Quantity": quantity,

            "Unit Price": float(unit_price),

            "Payment Method": payment_method,

            "Rating": float(rating),

            "Sales": float(sales)
        })


        transaction_id += 1


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(rows)


# ============================================================
# FORCE EXACT PAYMENT COUNT
# ============================================================

# Set all transactions to Cash first
df["Payment Method"] = "Cash"

# Select exactly 127 rows for UPI
upi_indexes = list(df.index[:UPI_COUNT])

for index in upi_indexes:

    df.loc[index, "Payment Method"] = "UPI"


# Remaining transactions
remaining_indexes = [
    index
    for index in df.index
    if index not in upi_indexes
]


# Alternate other payment methods
other_methods = [
    "Credit Card",
    "Debit Card"
]

for i, index in enumerate(remaining_indexes):

    df.loc[index, "Payment Method"] = (
        other_methods[i % len(other_methods)]
    )


# ============================================================
# FORCE EXACT AVERAGE RATING = 3.99
# ============================================================

# We need:
#
# 500 × 3.99 = 1995 total rating points
#
# Use 3.0 as starting rating.
# Then distribute additional rating points.

ratings = [Decimal("3.0")] * NUM_ROWS

target_rating_total = Decimal("1995.0")

remaining_rating = (
    target_rating_total -
    sum(ratings)
)


index = 0

while remaining_rating > 0:

    possible_addition = min(
        Decimal("2.0"),
        remaining_rating
    )

    ratings[index] += possible_addition

    remaining_rating -= possible_addition

    index += 1


df["Rating"] = [
    float(value)
    for value in ratings
]


# ============================================================
# SAVE DATASET
# ============================================================

project_root = Path(__file__).resolve().parent.parent

data_folder = project_root / "data"

data_folder.mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    data_folder /
    "supermarket_sales.csv"
)


df.to_csv(
    output_file,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 60)
print("SUPERMARKET SALES DATASET CREATED")
print("=" * 60)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print()
print("File:")
print(output_file)

print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)


cheese_sales = df.loc[
    df["Product"] == "Cheese",
    "Sales"
].sum()


branch_c_sales = df.loc[
    df["Branch"] == "C",
    "Sales"
].sum()


beverage_sales = df.loc[
    df["Category"] == "Beverages",
    "Sales"
].sum()


upi_transactions = (
    df["Payment Method"] == "UPI"
).sum()


member_average = df.loc[
    df["Customer Type"] == "Member",
    "Sales"
].mean()


normal_average = df.loc[
    df["Customer Type"] == "Normal",
    "Sales"
].mean()


average_rating = df["Rating"].mean()


print(
    f"Cheese Sales       : ₹{cheese_sales:,.2f}"
)

print(
    f"Branch C Sales     : ₹{branch_c_sales:,.2f}"
)

print(
    f"Beverages Sales    : ₹{beverage_sales:,.2f}"
)

print(
    f"UPI Transactions   : {upi_transactions}"
)

print(
    f"Member Average     : ₹{member_average:,.2f}"
)

print(
    f"Normal Average     : ₹{normal_average:,.2f}"
)

print(
    f"Average Rating     : {average_rating:.2f}"
)


# ============================================================
# FINAL CHECK
# ============================================================

print()
print("=" * 60)

checks = {

    "Rows = 500":
        len(df) == 500,

    "Cheese = ₹27,906.30":
        round(cheese_sales, 2) == 27906.30,

    "Branch C = ₹72,469.45":
        round(branch_c_sales, 2) == 72469.45,

    "Beverages = ₹56,108.24":
        round(beverage_sales, 2) == 56108.24,

    "UPI = 127":
        upi_transactions == 127,

    "Member average = ₹483.14":
        round(member_average, 2) == 483.14,

    "Normal average = ₹497.07":
        round(normal_average, 2) == 497.07,

    "Average rating = 3.99":
        round(average_rating, 2) == 3.99
}


all_passed = True

for name, passed in checks.items():

    if passed:
        print(f"PASS  ✓  {name}")

    else:
        print(f"FAIL  ✗  {name}")
        all_passed = False


print("=" * 60)

if all_passed:

    print("ALL PROJECT REQUIREMENTS PASSED ✓")

else:

    print("SOME REQUIREMENTS FAILED ✗")

print("=" * 60)