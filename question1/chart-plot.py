import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the colors
DARK_TEAL = "#008080"
DARK_RED = "#CC3239"
# Set figure aesthetics
sns.set_theme(style="whitegrid")

# ----------------------------------------------------------------------
# 1. LOAD AND PREPARE DATA
# ----------------------------------------------------------------------

try:
    df = pd.read_csv("./data/q1_rollup_results.csv")
except FileNotFoundError:
    print(
        "Error: The file 'q1_rollup_results.csv' was not found. Please ensure your query results are saved to this file."
    )
    exit()

# Clean up column names and null values
df.columns = df.columns.str.strip()
df = df.replace("[NULL]", np.nan).replace("", np.nan)
df["SALES_MONTH"] = df["SALES_MONTH"].astype(str).str.strip().str.capitalize()
df["calender week"] = pd.to_numeric(df["calender week"])

# Define the correct order for months
month_order = ["March", "April", "May"]

# Filter Data for Charts:
# 1. Monthly Totals (for Bar Chart): where 'calender week' is NaN
df_monthly = df[df["calender week"].isna()].copy()
df_monthly = df_monthly[df_monthly["SALES_MONTH"].isin(month_order)]
df_monthly["SALES_MONTH"] = pd.Categorical(
    df_monthly["SALES_MONTH"], categories=month_order, ordered=True
)
df_monthly = df_monthly.sort_values("SALES_MONTH")

# 2. Weekly Totals (for Line Chart): where 'calender week' is NOT NaN
df_weekly = df[df["calender week"].notna()].copy()
df_weekly["Weekly_Label"] = (
    df_weekly["SALES_MONTH"]
    + " Wk "
    + df_weekly["calender week"].astype(int).astype(str)
)
# Sort weekly data chronologically
df_weekly["Month_Num"] = df_weekly["SALES_MONTH"].apply(lambda x: month_order.index(x))
df_weekly = df_weekly.sort_values(by=["Month_Num", "calender week"])


# ----------------------------------------------------------------------
# CHART 1: MONTHLY VOLUME CONTRIBUTION (Vertical Bar with Trendline)
# ----------------------------------------------------------------------

plt.figure(figsize=(12, 7))
ax = plt.gca()

# Plot 1: Monthly Volume (Vertical BAR CHART)
sns.barplot(
    x="SALES_MONTH",
    y="DIGITAL_SEARCH_COUNT",
    data=df_monthly,
    color=DARK_TEAL,
    alpha=0.9,
    ax=ax,
    label="Monthly Volume",
    width=0.4,
)

# Plot 2: Trendline (LINE PLOT) - Overlay on the same axis
ax.plot(
    df_monthly["SALES_MONTH"],
    df_monthly["DIGITAL_SEARCH_COUNT"],
    color=DARK_RED,
    linestyle="-",
    marker="o",
    linewidth=2,
    label="Month-to-Month Trend",
    zorder=5,  # Ensures the line is plotted on top of the bars
)

# Add Data Labels (CRITICAL FIX for Vertical alignment)
for index, row in df_monthly.iterrows():
    ax.text(
        row["SALES_MONTH"],
        index,  # Y position is the categorical index (0, 1, 2)
        f" {row['DIGITAL_SEARCH_COUNT']:,}",  # Format count with thousands separator
        color="black",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

ax.set_title("Q1 Volume: Monthly Contribution and Trend", fontsize=16)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Total Digital Search Volume", fontsize=12)
ax.grid(axis="x", linestyle="--", alpha=0.7)
ax.legend(loc="upper right")

plt.tight_layout()
plt.savefig("question1/q1_monthly_bar_volume.png", bbox_inches="tight")
plt.close()


# ----------------------------------------------------------------------
# CHART 2: WEEKLY TREND (Line Chart)
# ----------------------------------------------------------------------

plt.figure(figsize=(14, 6))
sns.lineplot(
    x=df_weekly["Weekly_Label"],
    y="DIGITAL_SEARCH_COUNT",
    data=df_weekly,
    color=DARK_TEAL,
    linestyle="-",
    marker="o",
    linewidth=2,
)
plt.title("Q1 Trend: Weekly Fluctuation in Digital Commerce Searches", fontsize=16)
plt.xlabel("Calendar Week (March - May 2006)", fontsize=12)
plt.ylabel("Total Digital Search Count", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=9)
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("question1/q1_weekly_line_trend.png", bbox_inches="tight")
plt.close()

print("Successfully generated q1_monthly_bar_volume.png and q1_weekly_line_trend.png")
