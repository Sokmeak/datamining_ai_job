import pandas as pd
import numpy as np
from datetime import datetime

# Load the South Korea jobs dataset
df = pd.read_excel('south_korea_jobs.xlsx')

print("="*80)
print("DASHBOARD IMPLEMENTATION GUIDE FOR SOUTH KOREA AI JOBS")
print("="*80)

# ============================================================================
# PAGE 1 — EXECUTIVE OVERVIEW (Market Snapshot)
# ============================================================================
print("\n" + "="*80)
print("PAGE 1 — EXECUTIVE OVERVIEW")
print("="*80)

# Key KPIs
total_jobs = len(df)
today = pd.Timestamp(datetime.now())
active_jobs = len(df[df['application_deadline'] >= today])
avg_salary = df['salary_usd'].mean()
remote_jobs_pct = (len(df[df['remote_ratio'] > 0]) / total_jobs) * 100
avg_experience = df['years_experience'].mean()

print("\n📊 KEY KPIs:")
print(f"  • Total AI Jobs: {total_jobs:,}")
print(f"  • Active Job Openings: {active_jobs:,}")
print(f"  • Average Salary (USD): ${avg_salary:,.2f}")
print(f"  • Remote Jobs %: {remote_jobs_pct:.1f}%")
print(f"  • Avg Required Experience: {avg_experience:.1f} years")

print("\n📈 VISUAL 1: AI Job Postings Over Time")
print("  Implementation:")
df['posting_month'] = df['posting_date'].dt.to_period('M')
jobs_over_time = df.groupby('posting_month').size().reset_index(name='job_count')
print(f"  - Data points: {len(jobs_over_time)} months")
print(f"  - Date range: {df['posting_date'].min().date()} to {df['posting_date'].max().date()}")
print("  - Code: df.groupby(df['posting_date'].dt.to_period('M')).size()")

print("\n📈 VISUAL 2: Jobs by Role (Top 10)")
print("  Implementation:")
jobs_by_role = df['job_title'].value_counts().head(10)
print(jobs_by_role.to_string())
print("  - Code: df['job_title'].value_counts().head(10)")

print("\n📈 VISUAL 3: Jobs by Industry")
print("  Implementation:")
jobs_by_industry = df['industry'].value_counts()
print(jobs_by_industry.head(10).to_string())
print(f"  - Total industries: {len(jobs_by_industry)}")
print("  - Code: df['industry'].value_counts()")

# ============================================================================
# PAGE 2 — SALARY & EXPERIENCE INSIGHTS
# ============================================================================
print("\n\n" + "="*80)
print("PAGE 2 — SALARY & EXPERIENCE INSIGHTS")
print("="*80)

# Key KPIs
median_salary = df['salary_usd'].median()
min_salary = df['salary_usd'].min()
max_salary = df['salary_usd'].max()

# Calculate Senior Salary Premium
salary_by_exp = df.groupby('experience_level')['salary_usd'].mean()
print("\n📊 KEY KPIs:")
print(f"  • Median Salary (USD): ${median_salary:,.2f}")
print(f"  • Salary Range: ${min_salary:,} - ${max_salary:,}")
print(f"  • Salary by Experience Level:")
for level, sal in salary_by_exp.items():
    print(f"      - {level}: ${sal:,.2f}")
if 'SE' in salary_by_exp.index and 'EN' in salary_by_exp.index:
    senior_premium = salary_by_exp['SE'] - salary_by_exp['EN']
    print(f"  • Senior Salary Premium: ${senior_premium:,.2f}")

print("\n📈 VISUAL 1: Salary by Job Role (Top 15)")
print("  Implementation:")
salary_by_role = df.groupby('job_title')['salary_usd'].mean().sort_values(ascending=False).head(15)
print(salary_by_role.to_string())
print("  - Code: df.groupby('job_title')['salary_usd'].mean().sort_values(ascending=False)")

print("\n📈 VISUAL 2: Salary by Experience Level")
print("  Implementation:")
print(salary_by_exp.sort_values(ascending=False).to_string())
print("  - Code: df.groupby('experience_level')['salary_usd'].mean()")
print("  - Can also use boxplot: df.boxplot(column='salary_usd', by='experience_level')")

print("\n📈 VISUAL 3: Salary vs Years of Experience")
print("  Implementation:")
print(f"  - Data points: {len(df)} jobs")
print(f"  - Experience range: {df['years_experience'].min()} - {df['years_experience'].max()} years")
print(f"  - Company sizes available: {df['company_size'].unique()}")
print("  - Code: plt.scatter(df['years_experience'], df['salary_usd'], c=df['company_size'])")

print("\n📈 VISUAL 4: Remote vs Onsite Salary")
print("  Implementation:")
remote_salary = df.groupby('remote_ratio')['salary_usd'].mean().sort_index()
print(remote_salary.to_string())
print("  - Code: df.groupby('remote_ratio')['salary_usd'].mean()")

# ============================================================================
# PAGE 3 — SKILLS, QUALITY & JOB ATTRACTIVENESS
# ============================================================================
print("\n\n" + "="*80)
print("PAGE 3 — SKILLS, QUALITY & JOB ATTRACTIVENESS")
print("="*80)

# Parse required_skills (comma-separated)
all_skills = []
for skills_str in df['required_skills'].dropna():
    skills = [s.strip() for s in str(skills_str).split(',')]
    all_skills.extend(skills)

skills_count = pd.Series(all_skills).value_counts()
avg_benefits = df['benefits_score'].mean()
high_quality_threshold = 7.0  # Example threshold
high_quality_jobs_pct = (len(df[df['benefits_score'] >= high_quality_threshold]) / total_jobs) * 100

print("\n📊 KEY KPIs:")
print(f"  • Total Unique Skills: {len(skills_count)}")
print(f"  • Most Demanded Skill: {skills_count.index[0]} ({skills_count.iloc[0]} jobs)")
print(f"  • Avg Benefits Score: {avg_benefits:.2f}")
print(f"  • High-Quality Jobs % (score ≥{high_quality_threshold}): {high_quality_jobs_pct:.1f}%")

print("\n📈 VISUAL 1: Top 10 Required Skills")
print("  Implementation:")
top_skills = skills_count.head(10)
print(top_skills.to_string())
print("  - Code: Split required_skills, count occurrences")

print("\n📈 VISUAL 2: Skill vs Salary Premium (Top 10 Skills)")
print("  Implementation:")
# Calculate average salary for jobs requiring each top skill
skill_salary = {}
for skill in top_skills.index[:10]:
    jobs_with_skill = df[df['required_skills'].str.contains(skill, na=False, case=False)]
    if len(jobs_with_skill) > 0:
        skill_salary[skill] = jobs_with_skill['salary_usd'].mean()

skill_salary_series = pd.Series(skill_salary).sort_values(ascending=False)
print(skill_salary_series.to_string())
print("  - Code: Filter jobs by skill, calculate mean salary")

print("\n📈 VISUAL 3: Job Description Length vs Salary")
print("  Implementation:")
print(f"  - Description length range: {df['job_description_length'].min()} - {df['job_description_length'].max()} chars")
correlation = df[['job_description_length', 'salary_usd']].corr().iloc[0, 1]
print(f"  - Correlation: {correlation:.3f}")
print("  - Code: plt.scatter(df['job_description_length'], df['salary_usd'])")

print("\n📈 VISUAL 4: Benefits Score by Employment Type")
print("  Implementation:")
benefits_by_type = df.groupby('employment_type')['benefits_score'].mean().sort_values(ascending=False)
print(benefits_by_type.to_string())
print("  - Code: df.groupby('employment_type')['benefits_score'].mean()")

# ============================================================================
# ADDITIONAL INSIGHTS & RECOMMENDATIONS
# ============================================================================
print("\n\n" + "="*80)
print("IMPLEMENTATION RECOMMENDATIONS")
print("="*80)

print("\n🔧 TOOLS YOU CAN USE:")
print("  1. Power BI / Tableau:")
print("     - Import south_korea_jobs.xlsx")
print("     - Create calculated columns for skills (split required_skills)")
print("     - Use built-in visuals for charts")
print()
print("  2. Python (Matplotlib/Seaborn/Plotly):")
print("     - More customization and control")
print("     - Can create interactive dashboards with Plotly Dash or Streamlit")
print()
print("  3. Excel:")
print("     - Pivot tables for aggregations")
print("     - Charts for visualizations")
print("     - Slicers for filters")

print("\n📝 DATA PREPARATION NEEDED:")
print("  1. Skills Table:")
print("     - Split 'required_skills' into separate rows")
print("     - Create a skill dimension table")
print()
print("  2. Date Dimensions:")
print("     - Extract year, month, quarter from posting_date")
print("     - Calculate 'is_active' based on application_deadline")
print()
print("  3. Calculated Fields:")
print("     - remote_category: '0' → 'Onsite', '50' → 'Hybrid', '100' → 'Remote'")
print("     - salary_range_category: bin salaries into ranges")
print("     - experience_category: group years_experience")

print("\n✅ NEXT STEPS:")
print("  1. Choose your visualization tool (Power BI/Python/Excel)")
print("  2. Run data preprocessing (especially for skills)")
print("  3. Create calculated columns as needed")
print("  4. Build visuals page by page")
print("  5. Add interactive filters as specified")

print("\n" + "="*80)
print("Analysis complete! Run this script to see the data structure for your dashboard.")
print("="*80)
