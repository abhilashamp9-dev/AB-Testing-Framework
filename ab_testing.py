import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load datasets
control = pd.read_csv("control_group.csv", sep=";")
test = pd.read_csv("test_group.csv", sep=";")

# Add group labels
control["group"] = "Control"
test["group"] = "Test"

# Combine datasets
df = pd.concat([control, test], ignore_index=True)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace("# of ", "", regex=False)
    .str.replace(" ", "_", regex=False)
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.lower()
)

# Convert purchase column to numeric
df["purchase"] = pd.to_numeric(df["purchase"], errors="coerce")

# Remove rows with missing values
df = df.dropna(subset=["purchase"])

# Calculate average purchases for each group
performance = df.groupby("group")["purchase"].mean()

print("Average Purchases:")
print(performance.round(2))

# Perform independent t-test
control_values = df[df["group"] == "Control"]["purchase"]
test_values = df[df["group"] == "Test"]["purchase"]

t_stat, p_value = ttest_ind(control_values, test_values)

print("\nP-value:", round(p_value, 6))

if p_value < 0.05:
    print("Result: Statistically significant difference between groups.")
else:
    print("Result: No statistically significant difference between groups.")

# Calculate lift percentage
lift = (
    (performance["Test"] - performance["Control"])
    / performance["Control"]
) * 100

print(f"Lift: {lift:.2f}%")

# Create and save visualization
performance.plot(kind="bar")
plt.ylabel("Average Purchases")
plt.title("Control vs Test Average Purchases")
plt.tight_layout()
plt.savefig("conversion_rates.png")
plt.show()

