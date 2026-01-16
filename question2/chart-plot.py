import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set figure aesthetics
sns.set_theme(style="whitegrid")

# Load the data from the CSV file
try:
    df = pd.read_csv("./data/question2-data.csv")
except FileNotFoundError:
    print(
        "Error: The file 'question2-data.csv' was not found. Please ensure your query results are saved to this file."
    )
    exit()

# Clean up column names and null values from ROLLUP/GROUPING SETS
df.columns = df.columns.str.strip()
df["CATEGORY"] = df["CATEGORY"].str.strip()
# Replace SQL's [NULL] or empty strings with NaN for filtering
df = df.replace("[NULL]", np.nan).replace("", np.nan)

# Ensure 'hour' is numeric for plotting
df["hour"] = pd.to_numeric(df["hour"])
# ----------------------------------------------------------------------
# CHART 1: RANKED BAR CHART (Overall Category CTR)
# ----------------------------------------------------------------------

# Filter data for the (CATEGORY) grouping set: where both hour and weekday are NULL/NaN
df_overall_ctr = df[df["hour"].isna() & df["weekday"].isna()].copy()
df_overall_ctr = df_overall_ctr[
    df_overall_ctr["CATEGORY"].notna()
]  # Exclude the Grand Total [NULL] category

# Sort the data by CTR_Percentage in descending order for ranking
df_overall_ctr = df_overall_ctr.sort_values(by="CTR_PERCENTAGE", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_overall_ctr,
    x="CTR_PERCENTAGE",
    y="CATEGORY",
    hue="CATEGORY",
    palette="dark:#32B8B8",
)
plt.title("Overall User Intent (CTR) by Digital Commerce Category", fontsize=16)
plt.xlabel("Click-Through Rate (%)")
plt.ylabel("Digital Commerce Category")
plt.xticks(rotation=0)
plt.gca().xaxis.grid(True)  # Ensure horizontal grid lines are visible for comparison
plt.savefig("question2/q2_bar_category_ctr.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 2: HEATMAP (Category vs. Hour)
# ----------------------------------------------------------------------

# Filter data for the (CATEGORY, hour) grouping set (where weekday is NULL)
df_heatmap = df[df["weekday"].isna()].copy()
df_heatmap = df_heatmap[df_heatmap["hour"].notna()]

# print(df_heatmap.head(50))

# Pivot the data for the heatmap: CATEGORY (index) vs. hour (columns)
heatmap_data = df_heatmap.pivot(
    index="CATEGORY", columns="hour", values="CTR_PERCENTAGE"
)

plt.figure(figsize=(14, 7))
sns.heatmap(
    heatmap_data,
    cmap="viridis",
    annot=True,
    fmt=".1f",
    linewidths=0.5,
    cbar_kws={"label": "CTR Percentage (%)"},
)
plt.title("Peak Digital Commerce User Intent (CTR) by Category and Hour", fontsize=16)
plt.ylabel("Digital Commerce Category")
plt.xlabel("Hour of Day (00 - 23)")
plt.yticks(rotation=0)
plt.savefig("question2/q2_heatmap_hour_ctr.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 3: GROUPED BAR CHART (Category vs. Weekday)
# ----------------------------------------------------------------------

# Filter data for the (CATEGORY, weekday) grouping set (where hour is NULL)
df_bar = df[df["hour"].isna()].copy()
df_bar = df_bar[df_bar["weekday"].notna()]

# Define the correct order for the weekdays
weekday_order = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
# Ensure the weekday data is clean and set the category names to title case for the legend
df_bar["weekday"] = df_bar["weekday"].str.lower().str.strip()
df_bar["weekday"] = pd.Categorical(
    df_bar["weekday"], categories=weekday_order, ordered=True
)
df_bar = df_bar.sort_values("weekday")

plt.figure(figsize=(12, 7))
sns.barplot(
    data=df_bar,
    x="weekday",
    y="TOTAL_SEARCHES",
    hue="CATEGORY",
    palette="Spectral",
)
plt.title(
    "Total Digital Commerce Search Volume by Category and Day of Week", fontsize=16
)
plt.xlabel("Day of the Week")
plt.ylabel("Total Searches (Count)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Category", loc="upper left")
plt.savefig("question2/q2_bar_weekday_volume.png", bbox_inches="tight")
plt.close()

print(
    "Successfully generated q2_bar_category_ctr.png, q2_heatmap_hour_ctr.png and q2_bar_weekday_volume.png"
)
