import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/supermarket_sales.csv")

# Count each rating
rating_counts = (
    df["Rating"]
    .value_counts()
    .sort_index()
)

# Create chart
plt.figure(figsize=(8, 6))

rating_counts.plot(kind="bar")

plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig("charts/rating_distribution.png", dpi=300)

# Display chart
plt.show()

print("Rating Distribution chart created successfully!")