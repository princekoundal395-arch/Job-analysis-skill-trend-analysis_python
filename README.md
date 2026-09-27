# Data Analyst Job Market & Skills Trend Analysis

## Problem Statement
Which skills are actually most in-demand for Data Analyst roles? This project analyzes real job postings to find out which tools (SQL, Excel, Python, Power BI, Tableau) appear most frequently — helping job seekers prioritize what to learn first.

## Tools Used
- Python
- Pandas (data cleaning & analysis)
- Matplotlib (visualization)

## Dataset
`job_postings.csv` — 108 raw Data Analyst job postings (job title, company, location, description). The raw file intentionally contains real-world messiness: missing values, duplicate postings, and inconsistent location naming (e.g. "Bangalore" / "bangalore" / "BANGALORE" / "Bengaluru").

## Steps
1. Loaded job posting data using Pandas
2. **Cleaned and validated the data**:
   - Checked missing values in every column
   - Removed 8 exact duplicate postings
   - Standardized text columns (stripped whitespace, fixed casing)
   - Merged known location naming variants (e.g. "Bengaluru" → "Bangalore", "New Delhi" → "Delhi")
   - Dropped rows with an empty description, or missing location/company
   - Result: 108 raw rows → **91 clean rows** used for analysis
3. Searched each job description for 5 key skills: SQL, Excel, Python, Power BI, Tableau
4. Counted how many postings mentioned each skill
5. Converted counts into percentages
6. Visualized results using five different chart types:
   - **Bar chart** — overall demand (%) for each skill
   - **Pie chart** — share of total skill mentions
   - **Line chart** — cumulative job coverage as you learn skills in order of demand
   - **Scatter chart** — how many skills each individual job posting requires
   - **Grouped bar chart** — skill demand broken down by location

## Key Insight
Based on the cleaned dataset (91 postings), **Python (75.8%) and Power BI (74.7%)** are the most frequently requested skills, followed closely by **Excel (72.5%)**, **SQL (70.3%)**, and **Tableau (68.1%)** — all five skills are in fairly high and comparable demand rather than one or two tools dominating.

The **line chart** shows how quickly cumulative job coverage rises as you learn skills in order of demand. The **scatter chart** reveals that most postings ask for a mix of skills together rather than just one. The **grouped bar chart** shows demand for each skill varies noticeably by location — useful if you're job-hunting in a specific city.

## Result Charts
*(Sample output — when you run the script yourself, each chart pops up in its own window via `plt.show()` instead of being saved as a file.)*

![Bar Chart](chart_1.png)
![Pie Chart](chart_2.png)
![Line Chart](chart_3.png)
![Scatter Chart](chart_4.png)
![Grouped Bar Chart by Location](chart_5.png)

## How to Run
1. Make sure `job_postings.csv` and `analyze_skills.py` are in the same folder
2. Install requirements: `pip install pandas matplotlib`
3. Run: `python analyze_skills.py`
4. The terminal will print the cleaning steps and results, then each chart window will pop up one by one — **bar → pie → line → scatter → grouped bar**. Close a chart window to move on to the next one.

## Resume Bullet Point
> Cleaned and analyzed 100+ data analyst job postings using Python and Pandas (handling missing values, duplicates, and inconsistent text formatting) to identify in-demand skills; found Python and Power BI each mentioned in ~75% of listings, informing a skill-prioritization strategy for job preparation.
