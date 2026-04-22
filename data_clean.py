import pandas as pd

# ----------------------------
# LOAD DATA
# ----------------------------
# Make sure ds_salaries.csv is in the same folder as this script
df = pd.read_csv("ds_salaries.csv")

print("Raw data shape:", df.shape)
print("Columns:", df.columns.tolist())

# ----------------------------
# CLEAN & FILTER
# ----------------------------

# Keep only USD salaries for consistency
df = df[df["salary_currency"] == "USD"]

# Drop columns we don't need for the dashboard
df = df.drop(columns=["salary", "salary_currency"])

# Rename columns to be more readable in Power BI
df = df.rename(columns={
    "work_year":            "Year",
    "experience_level":     "Experience Level",
    "employment_type":      "Employment Type",
    "job_title":            "Job Title",
    "salary_in_usd":        "Salary (USD)",
    "employee_residence":   "Employee Country",
    "remote_ratio":         "Remote Ratio",
    "company_location":     "Company Country",
    "company_size":         "Company Size"
})

# Map coded values to readable labels
df["Experience Level"] = df["Experience Level"].map({
    "EN": "Entry-Level",
    "MI": "Mid-Level",
    "SE": "Senior",
    "EX": "Executive"
})

df["Employment Type"] = df["Employment Type"].map({
    "FT": "Full-Time",
    "PT": "Part-Time",
    "CT": "Contract",
    "FL": "Freelance"
})

df["Company Size"] = df["Company Size"].map({
    "S": "Small",
    "M": "Medium",
    "L": "Large"
})

df["Remote Ratio"] = df["Remote Ratio"].map({
    0:   "On-Site",
    50:  "Hybrid",
    100: "Fully Remote"
})

# ----------------------------
# ADD USEFUL COLUMNS
# ----------------------------

# Salary buckets for grouping in Power BI
def salary_bucket(sal):
    if sal < 60000:
        return "Under $60K"
    elif sal < 100000:
        return "$60K–$100K"
    elif sal < 150000:
        return "$100K–$150K"
    elif sal < 200000:
        return "$150K–$200K"
    else:
        return "$200K+"

df["Salary Range"] = df["Salary (USD)"].apply(salary_bucket)

# Flag US vs international companies
df["US Company"] = df["Company Country"].apply(lambda x: "US" if x == "US" else "International")

# ----------------------------
# DROP NULLS & DUPLICATES
# ----------------------------
df = df.dropna()
df = df.drop_duplicates()

# ----------------------------
# SUMMARY STATS (for your reference)
# ----------------------------
print("\n--- Cleaned Data Summary ---")
print("Rows after cleaning:", len(df))
print("\nExperience Level counts:")
print(df["Experience Level"].value_counts())
print("\nTop 10 Job Titles:")
print(df["Job Title"].value_counts().head(10))
print("\nAverage Salary by Experience Level:")
print(df.groupby("Experience Level")["Salary (USD)"].mean().sort_values(ascending=False).round(0))

# ----------------------------
# EXPORT
# ----------------------------
df.to_csv("ds_salaries_clean.csv", index=False)
print("\nDone! Saved to ds_salaries_clean.csv")