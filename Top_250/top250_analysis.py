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

# Redirect console output to a file (report_top250.txt)
class Logger(object):
    def __init__(self, filename="report_top250.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")  # Open in write mode

    def write(self, message):
        self.terminal.write(message)  # Print to console
        self.log.write(message)  # Write to file

    def flush(self):
        pass

# Apply redirection
sys.stdout = Logger("report_top250.txt")

print("Top 250 Restaurant Analysis Report\n")

# Load Top 250 Dataset
df_top250 = pd.read_csv("source/Top250.csv")  # Ensure the file is in the correct folder
print("\n First 5 Rows of Dataset:")
print(df_top250.head())

# Data Cleaning & Preprocessing
df_top250.dropna(inplace=True)  # Drop missing values
df_top250["Sales"] = df_top250["Sales"].astype(float)  # Convert sales to float
df_top250["YOY_Sales"] = df_top250["YOY_Sales"].str.rstrip('%').astype(float)  # Convert % to float
df_top250["Units"] = df_top250["Units"].astype(int)  # Convert units to int
df_top250["YOY_Units"] = df_top250["YOY_Units"].str.rstrip('%').astype(float)  # Convert % to float

# Exploratory Data Analysis (EDA)
# Sales Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_top250["Sales"], bins=30, kde=True)
plt.title("Sales Distribution (Top 250)")
plt.xlabel("Total Sales ($)")
plt.ylabel("Count")
plt.savefig("generated_charts/top250_sales_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# YOY Sales Growth Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_top250["YOY_Sales"], bins=20, kde=True)
plt.title("YOY Sales Growth Distribution (Top 250)")
plt.xlabel("YOY Sales Growth (%)")
plt.ylabel("Count")
plt.savefig("generated_charts/top250_yoy_sales_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# YOY Units Growth Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_top250["YOY_Units"], bins=20, kde=True)
plt.title("YOY Unit Growth Distribution (Top 250)")
plt.xlabel("YOY Unit Growth (%)")
plt.ylabel("Count")
plt.savefig("generated_charts/top250_yoy_units_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# Top Restaurant Segments
top_segments = df_top250["Segment_Category"].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_segments.index, y=top_segments.values)
plt.xticks(rotation=45)
plt.title("Top 10 Restaurant Segments (Top 250)")
plt.xlabel("Segment")
plt.ylabel("Number of Restaurants")
plt.savefig("generated_charts/top250_top_segments.png", dpi=300, bbox_inches='tight')
plt.show()

# Top-Performing Restaurants
# Top 10 Restaurants by Sales
top_sales = df_top250[["Restaurant", "Sales"]].sort_values(by="Sales", ascending=False).head(10)
print("\n Top 10 Restaurants by Sales:")
print(top_sales.to_string(index=False))

# Top 10 Restaurants by YOY Sales Growth
top_yoy_sales = df_top250[["Restaurant", "YOY_Sales"]].sort_values(by="YOY_Sales", ascending=False).head(10)
print("\n Top 10 Restaurants by YOY Sales Growth:")
print(top_yoy_sales.to_string(index=False))

# Top 10 Restaurants by Units
top_units = df_top250[["Restaurant", "Units"]].sort_values(by="Units", ascending=False).head(10)
print("\n Top 10 Restaurants by Total Units:")
print(top_units.to_string(index=False))

# Top 10 Restaurants by YOY Unit Growth
top_yoy_units = df_top250[["Restaurant", "YOY_Units"]].sort_values(by="YOY_Units", ascending=False).head(10)
print("\n Top 10 Restaurants by YOY Unit Growth:")
print(top_yoy_units.to_string(index=False))

# Export Cleaned Data for Reporting
df_top250.to_csv("generated_clean_csv/cleaned_top250.csv", index=False)
top_sales.to_csv("generated_clean_csv/top_sales_top250.csv", index=False)
top_yoy_sales.to_csv("generated_clean_csv/top_yoy_sales_top250.csv", index=False)
top_units.to_csv("generated_clean_csv/top_units_top250.csv", index=False)
top_yoy_units.to_csv("generated_clean_csv/top_yoy_units_top250.csv", index=False)

print("\n Analysis Completed! Cleaned data and insights saved.")

# Restore default console output
sys.stdout = sys.__stdout__
