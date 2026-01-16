# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

# # Define the dark teal color
# DARK_TEAL_COLOR = "#008080"

# # Assuming df_top5 contains the results of the final Question 3 SQL query
# # Load data (if not already loaded in the environment)
# try:
#     df_top5 = pd.read_csv("./data/question3-data.csv")
#     df_top5.columns = df_top5.columns.str.strip()
#     df_top5["CATEGORY"] = df_top5["CATEGORY"].astype(str).str.strip()
#     df_top5 = df_top5.sort_values(
#         by=["CATEGORY", "DOMAIN_RANK_WITHIN_CATEGORY"], ascending=[True, True]
#     )
# except FileNotFoundError:
#     print("Error: The file './data/question3-data.csv' was not found.")
#     exit()

# # ----------------------------------------------------------------------
# # SMALL MULTIPLES VERTICAL RANKED BAR CHART (with Independent Y-Scales)
# # ----------------------------------------------------------------------

# plt.figure(figsize=(15, 12))

# g = sns.catplot(
#     data=df_top5,
#     # X-axis is the domain name
#     x="THISDOMAIN",
#     # Y-axis is the magnitude (Clicks)
#     y="DOMAIN_CLICK_COUNT",
#     # Facet by Category
#     col="CATEGORY",
#     kind="bar",
#     color=DARK_TEAL_COLOR,
#     col_wrap=2,  # Layout for 2 charts per row
#     height=4,
#     aspect=2,
#     # CRITICAL FIX: Allows each chart to have its own Y-axis range
#     sharey=False,
#     # CRITICAL FIX: Ensures X-axis labels (domains) are unique per plot
#     sharex=False,
# )

# # 1. FIX THE Y-AXIS SCALE ISSUE (Visibility for small categories)
# # 2. FIX THE X-AXIS LABEL ISSUE (Readability)

# for ax in g.axes.flatten():
#     # Rotate X-axis labels (Domains) for readability
#     ax.tick_params(axis="x", rotation=90)

#     # Add a title to show the current category being displayed
#     ax.set_title(ax.get_title(), fontsize=12)

#     # Optional: Clean up the Y-axis label (Seaborn repeats it)
#     ax.set_ylabel("Total Clicks (High Intent)", fontsize=10)
#     ax.set_xlabel("Domain", fontsize=10)

# g.fig.suptitle(
#     "Top 5 Clicked Domains Ranked by Digital Commerce Category", y=1.02, fontsize=18
# )
# plt.subplots_adjust(hspace=0.6, wspace=0.2)  # Adjust spacing between charts

# plt.savefig(
#     "question3/q3_small_multiples_vertical_independent_scale.png", bbox_inches="tight"
# )
# plt.close()

# print(
#     "Successfully generated q3_small_multiples_vertical_independent_scale.png with fixed scales and readable labels."
# )

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import os
import re

# Define the dark teal color
DARK_TEAL_COLOR = "#008080"

# Load data
try:
    df_top5 = pd.read_csv("./data/question3-data.csv")
    df_top5.columns = df_top5.columns.str.strip()
    df_top5["CATEGORY"] = df_top5["CATEGORY"].astype(str).str.strip()
    df_top5 = df_top5.sort_values(
        by=["CATEGORY", "DOMAIN_RANK_WITHIN_CATEGORY"], ascending=[True, True]
    )
except FileNotFoundError:
    print("Error: The file './data/question3-data.csv' was not found.")
    exit()

# Create directory for temporary images
temp_dir = "question3/temp_plots"
os.makedirs(temp_dir, exist_ok=True)

# Function to sanitize filenames
def sanitize_filename(name):
    """Remove or replace invalid characters for filenames"""
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Get unique categories
categories = df_top5['CATEGORY'].unique()
image_files = []

print("Generating individual plots...")

# Define consistent figure size for all plots
FIG_WIDTH = 12
FIG_HEIGHT = 8

# Generate individual plots for each category
for i, category in enumerate(categories):
    # Filter data for current category
    category_data = df_top5[df_top5['CATEGORY'] == category]
    
    # Create individual plot with consistent size
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    
    # Create bar plot
    sns.barplot(
        data=category_data,
        x="THISDOMAIN",
        y="DOMAIN_CLICK_COUNT",
        color=DARK_TEAL_COLOR,
        ax=ax
    )
    
    # Customize the plot
    plt.title(f"Top 5 Clicked Domains - {category}", fontsize=16, pad=20)
    plt.xlabel("Domain", fontsize=14)
    plt.ylabel("Total Clicks (High Intent)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add value labels on bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='bottom', 
                   xytext=(0, 8), textcoords='offset points',
                   fontsize=11,
                   fontweight='bold')
    
    # Adjust layout with consistent padding
    plt.tight_layout(pad=3.0)
    
    # Sanitize category name for filename
    safe_category = sanitize_filename(category)
    
    # Save individual plot with consistent DPI and bbox_inches
    filename = f"{temp_dir}/category_{i+1:02d}_{safe_category}.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight', facecolor='white')
    image_files.append(filename)
    plt.close()
    
    print(f"Generated plot for {category}")

# Create GIF from individual plots
print("Creating GIF...")

try:
    # Read all images and ensure consistent size
    images = []
    target_size = None
    
    # First pass: determine the maximum dimensions
    max_width, max_height = 0, 0
    for filename in image_files:
        img = imageio.imread(filename)
        height, width = img.shape[:2]
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    
    print(f"Target GIF dimensions: {max_width} x {max_height}")
    
    # Second pass: read and pad images to consistent size
    for filename in image_files:
        img = imageio.imread(filename)
        height, width = img.shape[:2]
        
        # If image is smaller than target, pad it
        if height < max_height or width < max_width:
            # Create a white background image of target size
            padded_img = np.ones((max_height, max_width, 3), dtype=np.uint8) * 255
            
            # Calculate padding to center the original image
            pad_top = (max_height - height) // 2
            pad_left = (max_width - width) // 2
            
            # Place original image in the center
            padded_img[pad_top:pad_top+height, pad_left:pad_left+width] = img
            images.append(padded_img)
        else:
            images.append(img)
    
    # Save as GIF
    gif_filename = "question3/category_plots_animation.gif"
    imageio.mimsave(gif_filename, images, duration=4000, loop=0)  # 4000ms = 4 seconds per frame
    
    print(f"Successfully created GIF: {gif_filename}")
    print(f"GIF contains {len(images)} frames")
    print(f"GIF dimensions: {max_width} x {max_height}")

except Exception as e:
    print(f"Error creating GIF: {e}")
    print("But individual plots were generated successfully.")
    
    # Alternative: Create a simple GIF without resizing
    print("Attempting alternative GIF creation method...")
    try:
        images = []
        for filename in image_files:
            images.append(imageio.imread(filename))
        
        gif_filename = "question3/category_plots_simple.gif"
        imageio.mimsave(gif_filename, images, duration=2000, loop=0)
        print(f"Successfully created simple GIF: {gif_filename}")
    except Exception as e2:
        print(f"Alternative method also failed: {e2}")

# Optional: Clean up temporary individual plot files
try:
    cleanup = input("Do you want to clean up the temporary individual plot files? (y/n): ")
    if cleanup.lower() == 'y':
        for filename in image_files:
            if os.path.exists(filename):
                os.remove(filename)
        # Only remove directory if it's empty
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
        print("Temporary files cleaned up.")
    else:
        print(f"Individual plot files saved in: {temp_dir}")
except:
    print(f"Individual plot files saved in: {temp_dir}")

# Generate the original combined plot for reference
print("\nGenerating combined reference plot...")
try:
    plt.figure(figsize=(15, 12))

    g = sns.catplot(
        data=df_top5,
        x="THISDOMAIN",
        y="DOMAIN_CLICK_COUNT",
        col="CATEGORY",
        kind="bar",
        color=DARK_TEAL_COLOR,
        col_wrap=2,
        height=4,
        aspect=2,
        sharey=False,
        sharex=False,
    )

    for ax in g.axes.flatten():
        ax.tick_params(axis="x", rotation=90)
        ax.set_title(ax.get_title(), fontsize=12)
        ax.set_ylabel("Total Clicks (High Intent)", fontsize=10)
        ax.set_xlabel("Domain", fontsize=10)

    g.fig.suptitle(
        "Top 5 Clicked Domains Ranked by Digital Commerce Category", y=1.02, fontsize=18
    )
    plt.subplots_adjust(hspace=0.6, wspace=0.2)

    plt.savefig(
        "question3/q3_small_multiples_vertical_independent_scale.png", 
        bbox_inches='tight',
        dpi=100
    )
    plt.close()
    print("Successfully generated combined reference plot: question3/q3_small_multiples_vertical_independent_scale.png")

except Exception as e:
    print(f"Error generating combined plot: {e}")

print("\nProcess completed!")