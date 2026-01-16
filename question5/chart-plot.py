import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# ====================================================================
# CUSTOMIZATION PARAMETERS
# ====================================================================
# TARGET_TICKER = "AAPL"  # Change to 'EBAY' to analyze eBay's stock trend
TARGET_TICKER = "EBAY"  # Change to 'EBAY' to analyze eBay's stock trend
FILE_NAME = f"./data/q5_correlation_results_{TARGET_TICKER}.csv"

# Colors for the dual axis
AOL_COLOR = "#008080"  # Dark Teal (Internal Trend)
STOCK_COLOR = "#FF9900"  # Accent Orange (External Trend)
# ====================================================================


# Set figure aesthetics
sns.set_theme(style="whitegrid")

# ----------------------------------------------------------------------
# 1. LOAD AND PREPARE DATA
# ----------------------------------------------------------------------

try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"Error: The file '{FILE_NAME}' was not found. Please check your file path.")
    exit()

# Clean and filter the data
df.columns = df.columns.str.strip()
df = df[df["TICKER"].str.strip() == TARGET_TICKER].copy()
df["DATE_KEY"] = pd.to_datetime(df["DATE_KEY"])

# Ensure data is sorted for a time series plot
df = df.sort_values("DATE_KEY")


# ----------------------------------------------------------------------
# 2. GENERATE DUAL-AXIS TIME SERIES
# ----------------------------------------------------------------------

fig, ax1 = plt.subplots(figsize=(16, 8))  # ax1 is the primary axis (AOL Trend)

# --- PRIMARY AXIS PLOT (AOL Cumulative Search Average) ---
sns.lineplot(
    x="DATE_KEY",
    y="CUMULATIVE_SEARCH_AVG",
    data=df,
    ax=ax1,
    color=AOL_COLOR,
    linewidth=2,
    label=f"AOL Cumulative Search Avg ({TARGET_TICKER})",
)
ax1.set_xlabel("Date (March 1 - May 31, 2006)", fontsize=12)
ax1.set_ylabel("Cumulative Daily Digital Searches (Avg)", color=AOL_COLOR, fontsize=12)
ax1.tick_params(axis="y", labelcolor=AOL_COLOR)
ax1.grid(axis="y", linestyle="--", alpha=0.5)


# --- SECONDARY AXIS PLOT (External Stock Price Trend) ---
ax2 = ax1.twinx()  # Create a second axes that shares the same x-axis

sns.lineplot(
    x="DATE_KEY",
    y="ADJ_CLOSE_PRICE",
    data=df,
    ax=ax2,
    color=STOCK_COLOR,
    linestyle="--",  # Differentiate the two lines
    linewidth=2,
    label=f"{TARGET_TICKER} Adj. Close Price (USD)",
)
ax2.set_ylabel(
    f"{TARGET_TICKER} Adjusted Close Price (USD)", color=STOCK_COLOR, fontsize=12
)
ax2.tick_params(axis="y", labelcolor=STOCK_COLOR)


# ----------------------------------------------------------------------
# 3. FINAL FORMATTING AND LEGEND
# ----------------------------------------------------------------------

ax1.set_title(
    f"Q5 Synthesis: AOL User Interest (Internal Signal) vs. {TARGET_TICKER} Stock Trend",
    fontsize=16,
)

# Format X-axis to show month names
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.xticks(rotation=45, ha="right")

# Combine Legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", fontsize=10)

plt.tight_layout()
plt.savefig(f"question5/q5_correlation_chart_{TARGET_TICKER}.png", bbox_inches="tight")
plt.close()

print(f"Successfully generated q5_correlation_chart_{TARGET_TICKER}.png")
