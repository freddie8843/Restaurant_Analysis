#Future 50 Analysis
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

# Redirect console output to a file (report.txt)
class Logger(object):
    def __init__(self, filename="report.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")  # Open in write mode

    def write(self, message):
        self.terminal.write(message)  # Print to console
        self.log.write(message)  # Write to file

    def flush(self):
        pass

# Apply redirection
sys.stdout = Logger("report.txt")

print("Future 50 Restaurant Analysis Report\n")

# 1️⃣ Load Future 50 Dataset
df_future50 = pd.read_csv("source/Future50.csv")  # Ensure the file is in the correct folder
print("\nFirst 5 Rows of Dataset:")
print(df_future50.head())

# 2️⃣ Data Cleaning & Preprocessing
df_future50['YOY_Sales'] = df_future50['YOY_Sales'].str.rstrip('%').astype(float)  # Convert % to float
df_future50['YOY_Units'] = df_future50['YOY_Units'].str.rstrip('%').astype(float)  # Convert % to float
df_future50['Franchising'] = df_future50['Franchising'].map({'Yes': 1, 'No': 0})  # Convert Yes/No to 1/0
df_future50['City'] = df_future50['Location'].apply(lambda x: x.split(',')[0])  # Extract city name

# 3️⃣ Exploratory Data Analysis (EDA)
# 🔹 Sales Growth Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_future50['YOY_Sales'], bins=20, kde=True)
plt.title("Year-Over-Year Sales Growth Distribution (Future 50)")
plt.xlabel("YOY Sales Growth (%)")
plt.ylabel("Count")
plt.savefig("generated_charts/sales_growth_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# 🔹 Unit Growth Distribution
plt.figure(figsize=(10,6))
sns.histplot(df_future50['YOY_Units'], bins=20, kde=True)
plt.title("Year-Over-Year Unit Growth Distribution (Future 50)")
plt.xlabel("YOY Unit Growth (%)")
plt.ylabel("Count")
plt.savefig("generated_charts/unit_growth_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

# 4️⃣ Franchising vs. Non-Franchising Analysis
# 🔹 Franchising Impact on Sales
plt.figure(figsize=(10,6))
sns.boxplot(x=df_future50['Franchising'], y=df_future50['YOY_Sales'])
plt.xticks([0,1], ["Non-Franchised", "Franchised"])
plt.title("Impact of Franchising on Sales Growth")
plt.ylabel("YOY Sales Growth (%)")
plt.savefig("generated_charts/franchising_sales.png", dpi=300, bbox_inches='tight')
plt.show()

# 🔹 Franchising Impact on Unit Growth
plt.figure(figsize=(10,6))
sns.boxplot(x=df_future50['Franchising'], y=df_future50['YOY_Units'])
plt.xticks([0,1], ["Non-Franchised", "Franchised"])
plt.title("Impact of Franchising on Unit Growth")
plt.ylabel("YOY Unit Growth (%)")
plt.savefig("generated_charts/franchising_unit_growth.png", dpi=300, bbox_inches='tight')
plt.show()

# 5️⃣ Top Cities for Fastest-Growing Restaurants
top_cities = df_future50['City'].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_cities.index, y=top_cities.values)
plt.xticks(rotation=45)
plt.title("Top Cities with the Most Future 50 Restaurants (2020)")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")
plt.savefig("generated_charts/top_cities_fastest_growth.png", dpi=300, bbox_inches='tight')
plt.show()

# 6️⃣ Top-Performing Restaurants
# 🔹 Top 10 Fastest-Growing Restaurants (by YOY Sales)
top_growth = df_future50[['Restaurant', 'YOY_Sales']].sort_values(by='YOY_Sales', ascending=False).head(10)
print("\nTop 10 Fastest-Growing Restaurants:")
print(top_growth.to_string(index=False))

# 🔹 Top 10 Highest Revenue per Unit
top_unit_volume = df_future50[['Restaurant', 'Unit_Volume']].sort_values(by='Unit_Volume', ascending=False).head(10)
print("\nTop 10 Highest Revenue per Unit:")
print(top_unit_volume.to_string(index=False))

# 7️⃣ Small vs. Big Businesses (Sales & Units)
plt.figure(figsize=(10,6))
sns.scatterplot(x=df_future50['Units'], y=df_future50['Sales'], hue=df_future50['Franchising'])
plt.title("Sales vs. Units: Small vs. Big Businesses")
plt.xlabel("Number of Units")
plt.ylabel("Total Sales")
plt.savefig("generated_charts/small_vs_big_businesses.png", dpi=300, bbox_inches='tight')
plt.show()

# 8️⃣ Export Cleaned Data for Reporting
df_future50.to_csv("generated_clean_csv/cleaned_future50.csv", index=False)
top_growth.to_csv("generated_clean_csv/top_growing_restaurants.csv", index=False)
top_unit_volume.to_csv("generated_clean_csv/highest_revenue_per_unit.csv", index=False)

print("\nAnalysis Completed! Cleaned data and insights saved.")

# Restore default console output
sys.stdout = sys.__stdout__

#end of code