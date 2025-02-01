import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure necessary directories exist
directories = ["source", "generated_charts", "generated_clean_csv"]
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Redirect console output to a file (report_independent100.txt)
class Logger(object):
    def __init__(self, filename="report_independent100.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")  # Open in write mode

    def write(self, message):
        self.terminal.write(message)  # Print to console
        self.log.write(message)  # Write to file

    def flush(self):
        pass

# Apply redirection
sys.stdout = Logger("report_independent100.txt")

print(" Independent 100 Restaurant Analysis Report\n")

# Load Independent 100 Dataset
df_independent100 = pd.read_csv("source/Independence100.csv")  # Ensure the file is in the correct folder
print("\n First 5 Rows of Dataset:")
print(df_independent100.head())

# Data Cleaning & Preprocessing
df_independent100.dropna(inplace=True)  # Drop missing values
df_independent100["Sales"] = df_independent100["Sales"].astype(float)  # Convert sales to float
df_independent100["Average Check"] = df_independent100["Average Check"].astype(float)  # Convert check to float
df_independent100["Meals Served"] = df_independent100["Meals Served"].astype(int)  # Convert to int

# Exploratory Data Analysis (EDA)
# Sales Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_independent100["Sales"], bins=20, kde=True)
plt.title("Sales Distribution (Independent 100)")
plt.xlabel("Total Sales ($)")
plt.ylabel("Count")
plt.savefig("generated_charts/independent100_sales_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# Average Check Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_independent100["Average Check"], bins=20, kde=True)
plt.title("Average Check Distribution (Independent 100)")
plt.xlabel("Average Check ($)")
plt.ylabel("Count")
plt.savefig("generated_charts/independent100_avg_check_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# Meals Served Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_independent100["Meals Served"], bins=20, kde=True)
plt.title("Meals Served Distribution (Independent 100)")
plt.xlabel("Total Meals Served")
plt.ylabel("Count")
plt.savefig("generated_charts/independent100_meals_served_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# Top Cities for Most Independent Restaurants
top_cities = df_independent100["City"].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_cities.index, y=top_cities.values)
plt.xticks(rotation=45)
plt.title("Top Cities with Most Independent 100 Restaurants")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")
plt.savefig("generated_charts/independent100_top_cities.png", dpi=300, bbox_inches='tight')
plt.show()

# Top-Performing Restaurants
# Top 10 Restaurants by Sales
top_sales = df_independent100[["Restaurant", "Sales"]].sort_values(by="Sales", ascending=False).head(10)
print("\n Top 10 Restaurants by Sales:")
print(top_sales.to_string(index=False))

# Top 10 Restaurants by Average Check
top_avg_check = df_independent100[["Restaurant", "Average Check"]].sort_values(by="Average Check", ascending=False).head(10)
print("\n Top 10 Restaurants by Highest Average Check:")
print(top_avg_check.to_string(index=False))

# Top 10 Restaurants by Meals Served
top_meals_served = df_independent100[["Restaurant", "Meals Served"]].sort_values(by="Meals Served", ascending=False).head(10)
print("\n Top 10 Restaurants by Meals Served:")
print(top_meals_served.to_string(index=False))

# Export Cleaned Data for Reporting
df_independent100.to_csv("generated_clean_csv/cleaned_independent100.csv", index=False)
top_sales.to_csv("generated_clean_csv/top_sales_independent100.csv", index=False)
top_avg_check.to_csv("generated_clean_csv/top_avg_check_independent100.csv", index=False)
top_meals_served.to_csv("generated_clean_csv/top_meals_served_independent100.csv", index=False)

print("\n Analysis Completed! Cleaned data and insights saved.")

# Restore default console output
sys.stdout = sys.__stdout__
