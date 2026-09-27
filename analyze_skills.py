"""
Project: Data Analyst Job Market & Skills Trend Analysis
Level: Beginner
Tools: Python, Pandas, Matplotlib

WHAT THIS PROJECT DOES:
1. Reads a list of data analyst job postings (job_postings.csv)
2. Cleans the data with pandas (missing values, duplicates, text
   standardization) - real job data is rarely clean out of the box
3. Searches each job description for common skills (SQL, Excel, Python,
   Power BI, Tableau)
4. Counts how many job postings mention each skill
5. Shows the results as a percentage
6. Draws FIVE charts, one after another, using plt.show():
   - Bar chart      -> most in-demand skills (% of postings)
   - Pie chart      -> share of total skill mentions
   - Line chart     -> cumulative % of jobs covered as you learn top skills one by one
   - Scatter        -> how many skills each individual job posting asks for
   - Grouped bar     -> skill demand broken down by location

HOW TO RUN:
1. Make sure job_postings.csv is in the same folder as this file
2. Run: python analyze_skills.py
3. It will print the results in the terminal, then pop up each chart
   window one by one. Close a chart window to move on to the next one.
"""

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------
# STEP 1: Load the data
# -----------------------------------------------------
data = pd.read_csv("job_postings.csv")

print("Step 1: Data loaded")
print(f"Raw row count: {len(data)}")
print()

# -----------------------------------------------------
# STEP 2: Clean & validate the data (pandas)
# -----------------------------------------------------
print("Step 2: Data Cleaning & Validation")
print("-" * 40)

# 2a) Check for missing values in each column
print("Missing values per column (before cleaning):")
print(data.isnull().sum())

# 2b) Check for exact duplicate job postings
duplicate_count = data.duplicated().sum()
print(f"\nDuplicate rows found: {duplicate_count}")
if duplicate_count > 0:
    data = data.drop_duplicates()
    print(f"Removed {duplicate_count} duplicate rows.")

# 2c) Standardize text columns - strip whitespace, fix casing
# (protects against "Bangalore" vs " bangalore " vs "BANGALORE"
#  being treated as different locations)
for col in ["job_title", "company", "location"]:
    data[col] = data[col].str.strip()

data["location"] = data["location"].str.title()
# fix known naming variants that Title Case alone won't catch
data["location"] = data["location"].replace({"New Delhi": "Delhi", "Bengaluru": "Bangalore"})

# 2d) Drop rows with a missing/empty description - they can't be
# analyzed for skills, so they'd break the rest of the script
before_drop = len(data)
data["description"] = data["description"].replace("", pd.NA)
data = data.dropna(subset=["description"])
after_drop = len(data)
if before_drop != after_drop:
    print(f"Dropped {before_drop - after_drop} rows with empty description.")

# 2e) Drop rows with a missing location or company (can't be grouped/analyzed)
before_drop2 = len(data)
data["location"] = data["location"].replace("", pd.NA)
data["company"] = data["company"].replace("", pd.NA)
data = data.dropna(subset=["location", "company"])
after_drop2 = len(data)
if before_drop2 != after_drop2:
    print(f"Dropped {before_drop2 - after_drop2} rows with missing location/company.")

# 2f) Reset index after any row removal so downstream code
# (which uses row numbers for the scatter chart) stays correct
data = data.reset_index(drop=True)

print(f"\nData is now clean. Final row count: {len(data)}")
print(f"Unique locations: {sorted(data['location'].unique())}")
print("-" * 40)
print()

# -----------------------------------------------------
# STEP 3: Define the skills we want to search for
# -----------------------------------------------------
skills_to_check = ["SQL", "Excel", "Python", "Power BI", "Tableau"]

# -----------------------------------------------------
# STEP 4: Count how many job postings mention each skill
# -----------------------------------------------------
skill_counts = {}
skill_mask = {}  # True/False per job, per skill (needed for line & scatter charts)

for skill in skills_to_check:
    mask = data["description"].str.contains(skill, case=False)
    skill_mask[skill] = mask
    skill_counts[skill] = mask.sum()

print("Step 4: Skill mentions counted!")
print()

# -----------------------------------------------------
# STEP 5: Convert counts into percentages
# -----------------------------------------------------
total_jobs = len(data)
skill_percentages = {skill: round((count / total_jobs) * 100, 1)
                      for skill, count in skill_counts.items()}

# -----------------------------------------------------
# STEP 6: Print a simple summary table
# -----------------------------------------------------
print("Step 6: Final Results")
print("-" * 40)
print(f"{'Skill':<12}{'Job Count':<12}{'Percentage'}")
print("-" * 40)

sorted_skills = sorted(skill_percentages.items(), key=lambda x: x[1], reverse=True)

for skill, percentage in sorted_skills:
    count = skill_counts[skill]
    print(f"{skill:<12}{count:<12}{percentage}%")

print("-" * 40)
print()

skill_names = [item[0] for item in sorted_skills]
skill_values = [item[1] for item in sorted_skills]

# =======================================================
# CHART 1: BAR CHART - most in-demand skills (%)
# =======================================================
plt.figure(figsize=(8, 5))
plt.bar(skill_names, skill_values, color="#4C72B0")
plt.title("Most In-Demand Skills for Data Analyst Jobs")
plt.xlabel("Skill")
plt.ylabel("Percentage of Job Postings (%)")
plt.ylim(0, 100)
for i, value in enumerate(skill_values):
    plt.text(i, value + 1, f"{value}%", ha="center")
plt.tight_layout()
plt.show()
print("Chart 1 displayed: Bar Chart")

# =======================================================
# CHART 2: PIE CHART - share of total skill mentions
# =======================================================
plt.figure(figsize=(7, 7))
plt.pie(
    skill_values,
    labels=skill_names,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"],
)
plt.title("Share of Total Skill Mentions")
plt.tight_layout()
plt.show()
print("Chart 2 displayed: Pie Chart")

# =======================================================
# CHART 3: LINE CHART - cumulative job coverage
# If a job seeker learns skills in order of popularity,
# what % of job postings would they qualify for (mention
# AT LEAST one of the skills learned so far)?
# =======================================================
cumulative_mask = pd.Series(False, index=data.index)
cumulative_coverage = []

for skill, _ in sorted_skills:
    cumulative_mask = cumulative_mask | skill_mask[skill]
    coverage_pct = round((cumulative_mask.sum() / total_jobs) * 100, 1)
    cumulative_coverage.append(coverage_pct)

plt.figure(figsize=(8, 5))
plt.plot(skill_names, cumulative_coverage, marker="o", color="#55A868", linewidth=2)
plt.title("Cumulative Job Coverage as You Learn More Skills")
plt.xlabel("Skills Learned (in order of demand)")
plt.ylabel("% of Job Postings Covered")
plt.ylim(0, 105)
for i, value in enumerate(cumulative_coverage):
    plt.text(i, value + 2, f"{value}%", ha="center")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
print("Chart 3 displayed: Line Chart")

# =======================================================
# CHART 4: SCATTER CHART - skills required per job posting
# Shows, for each individual job posting, how many of the
# 5 tracked skills it mentions (skill "richness" per job).
# =======================================================
skills_per_job = pd.DataFrame(skill_mask).sum(axis=1)  # count of skills per row

plt.figure(figsize=(10, 5))
locations = sorted(data["location"].unique())
colors_cycle = plt.cm.tab10.colors
location_color = {loc: colors_cycle[i % len(colors_cycle)] for i, loc in enumerate(locations)}
point_colors = data["location"].map(location_color)

plt.scatter(range(1, total_jobs + 1), skills_per_job, c=point_colors, s=60, edgecolors="black")
plt.title("Number of Skills Required per Job Posting")
plt.xlabel("Job Posting # (row in dataset)")
plt.ylabel("Number of Tracked Skills Mentioned")
plt.ylim(0, len(skills_to_check) + 1)
plt.grid(True, alpha=0.3)

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=location_color[loc],
                       markeredgecolor='black', markersize=9, label=loc) for loc in locations]
plt.legend(handles=handles, title="Location", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()
print("Chart 4 displayed: Scatter Chart")

# =======================================================
# CHART 5: GROUPED BAR CHART - skill demand by location
# For each location, what % of postings there mention
# each skill? Helps spot regional differences in demand.
# =======================================================
import numpy as np

data["skills_found"] = [
    [skill for skill in skills_to_check if skill_mask[skill][i]]
    for i in range(total_jobs)
]

location_skill_pct = {}
for loc in locations:
    loc_jobs = data[data["location"] == loc]
    loc_total = len(loc_jobs)
    location_skill_pct[loc] = [
        round((skill_mask[skill][data["location"] == loc].sum() / loc_total) * 100, 1)
        for skill in skills_to_check
    ]

x = np.arange(len(skills_to_check))
n_locations = len(locations)
bar_width = 0.8 / n_locations

plt.figure(figsize=(11, 6))
for i, loc in enumerate(locations):
    offset = (i - n_locations / 2) * bar_width + bar_width / 2
    plt.bar(x + offset, location_skill_pct[loc], width=bar_width, label=loc)

plt.title("Skill Demand by Location (%)")
plt.xlabel("Skill")
plt.ylabel("Percentage of Local Postings (%)")
plt.xticks(x, skills_to_check)
plt.ylim(0, 110)
plt.legend(title="Location", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()
print("Chart 5 displayed: Grouped Bar Chart (Skill Demand by Location)")

print()
print("DONE! All 5 charts were displayed.")
