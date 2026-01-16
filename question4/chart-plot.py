import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Define the colors
DARK_TEAL = "#097157"
ACCENT_RED = "#12111B"  # A strong contrasting color for annotations
ACCENT_BLUE = "#ce1414"  # New color for unique users line

# Set figure aesthetics
sns.set_theme(style="whitegrid")

# ----------------------------------------------------------------------
# 1. LOAD AND PREPARE DATA
# ----------------------------------------------------------------------

try:
    # Load the overall daily search trend (Context)
    df_trend = pd.read_csv("./data/q4_daily_trend.csv")
    # Load the event day search volumes (Stimulus/Response)
    df_events = pd.read_csv("./data/q4_event_response.csv")
except FileNotFoundError:
    print(
        "Error: Required files (q4_daily_trend.csv and/or q4_event_response.csv) not found."
    )
    exit()

# Clean and convert date columns
df_trend.columns = df_trend.columns.str.strip()
df_events.columns = df_events.columns.str.strip()

# Convert the consistent date string to datetime objects
df_trend["EVENT_DATE_STRING"] = pd.to_datetime(df_trend["EVENT_DATE_STRING"])
df_events["EVENT_DATE"] = pd.to_datetime(df_events["EVENT_DATE"])


# Merge the event data into the trend data on the event date
df_merged = pd.merge(
    df_trend,
    df_events[["EVENT_DATE", "EVENT_KEYWORD", "HIGH_INTENT_SEARCH_COUNT"]],
    left_on="EVENT_DATE_STRING",
    right_on="EVENT_DATE",
    how="left",
)

# ----------------------------------------------------------------------
# 2. GENERATE ANNOTATED TIME SERIES CHART
# ----------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(16, 8))  # ax1 is the primary axis (Total Searches)

# --- PRIMARY AXIS PLOT (Total Searches) ---
sns.lineplot(
    x="EVENT_DATE_STRING",
    y="TOTAL_DAILY_DIGITAL_SEARCHES",
    data=df_merged,
    ax=ax1,
    color=DARK_TEAL,
    linewidth=1.5,
    label="Total Daily Digital Searches",
)
ax1.set_ylabel("Total Daily Digital Searches (Count)", color=DARK_TEAL, fontsize=12)
ax1.tick_params(axis="y", labelcolor=DARK_TEAL)
ax1.grid(axis="y", linestyle="--", alpha=0.7)


# --- SECONDARY AXIS PLOT (Unique Users) ---
ax2 = ax1.twinx()  # Create a second axes that shares the same x-axis

sns.lineplot(
    x="EVENT_DATE_STRING",
    y="UNIQUE_DAILY_DIGITAL_USERS",
    data=df_merged,
    ax=ax2,
    color=ACCENT_BLUE,
    linestyle="--",  # Differentiate the unique user line visually
    linewidth=1.5,
    label="Unique Daily Digital Users",
)
ax2.set_ylabel("Unique Daily Digital Users (Count)", color=ACCENT_BLUE, fontsize=12)
ax2.tick_params(axis="y", labelcolor=ACCENT_BLUE)


# --- EVENT ANNOTATIONS (Tied to the Primary Axis for visual placement) ---
df_annotations = df_merged[df_merged["HIGH_INTENT_SEARCH_COUNT"].notna()].copy()

ax1.scatter(
    df_annotations["EVENT_DATE_STRING"],
    df_annotations["TOTAL_DAILY_DIGITAL_SEARCHES"],
    color=ACCENT_RED,
    s=100,
    zorder=5,
    label="Search Volume on Event Day",
)

# Annotate each event point with its name
for index, row in df_annotations.iterrows():
    ax1.annotate(
        text=row["EVENT_KEYWORD"],
        xy=(row["EVENT_DATE_STRING"], row["TOTAL_DAILY_DIGITAL_SEARCHES"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color=ACCENT_RED,
        fontweight="bold",
    )

# ----------------------------------------------------------------------
# 3. FINAL CHART FORMATTING
# ----------------------------------------------------------------------

ax1.set_title(
    "Dual-Axis Analysis: Search Volume and Unique Users vs. External Events (Mar-May 2006)",
    fontsize=16,
)
ax1.set_xlabel("Date (March 1 - May 31, 2006)", fontsize=12)

# Format X-axis
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.xticks(rotation=45, ha="right")

# Combine Legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="lower right", fontsize=10)

plt.tight_layout()
plt.savefig("question4/q4_annotated_timeseries.png", bbox_inches="tight")
plt.close()

print("Successfully generated q4_annotated_timeseries.png")
