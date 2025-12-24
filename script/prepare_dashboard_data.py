import pandas as pd
import numpy as np
from datetime import datetime

"""
This script prepares the South Korea AI jobs data for dashboard creation.
It creates all necessary tables and calculated columns needed for the 3-page dashboard.
"""

# Load the filtered data
print("Loading South Korea AI jobs data...")
df = pd.read_excel('south_korea_jobs.xlsx')
print(f"✓ Loaded {len(df)} jobs\n")

# ============================================================================
# 1. MAIN JOBS TABLE - Add Calculated Columns
# ============================================================================
print("=" * 80)
print("PREPARING MAIN JOBS TABLE")
print("=" * 80)

# Add date dimensions
df['posting_year'] = df['posting_date'].dt.year
df['posting_month'] = df['posting_date'].dt.month
df['posting_quarter'] = df['posting_date'].dt.quarter
df['posting_year_month'] = df['posting_date'].dt.to_period('M').astype(str)

# Add active job flag
today = pd.Timestamp(datetime.now())
df['is_active'] = df['application_deadline'] >= today

# Categorize remote work
def categorize_remote(ratio):
    if ratio == 0:
        return 'Onsite'
    elif ratio == 100:
        return 'Remote'
    else:
        return 'Hybrid'

df['remote_category'] = df['remote_ratio'].apply(categorize_remote)

# Categorize salary ranges
df['salary_range'] = pd.cut(df['salary_usd'], 
                             bins=[0, 50000, 75000, 100000, 150000, 300000],
                             labels=['<50K', '50-75K', '75-100K', '100-150K', '>150K'])

# Categorize experience
def categorize_experience(years):
    if years <= 2:
        return 'Entry (0-2y)'
    elif years <= 5:
        return 'Mid (3-5y)'
    elif years <= 10:
        return 'Senior (6-10y)'
    else:
        return 'Expert (10+y)'

df['experience_category'] = df['years_experience'].apply(categorize_experience)

# Expand experience level names
experience_mapping = {
    'EN': 'Entry Level',
    'MI': 'Mid Level',
    'SE': 'Senior',
    'EX': 'Executive'
}
df['experience_level_full'] = df['experience_level'].map(experience_mapping).fillna(df['experience_level'])

# Categorize benefits quality
def categorize_benefits(score):
    if pd.isna(score):
        return 'Unknown'
    elif score >= 8:
        return 'Excellent (8+)'
    elif score >= 6:
        return 'Good (6-8)'
    elif score >= 4:
        return 'Average (4-6)'
    else:
        return 'Below Average (<4)'

df['benefits_category'] = df['benefits_score'].apply(categorize_benefits)

print(f"✓ Added calculated columns:")
print(f"  - Date dimensions: year, month, quarter, year_month")
print(f"  - is_active: {df['is_active'].sum()} active jobs")
print(f"  - remote_category: {df['remote_category'].value_counts().to_dict()}")
print(f"  - salary_range: {df['salary_range'].value_counts().sort_index().to_dict()}")
print(f"  - experience_category: {df['experience_category'].value_counts().to_dict()}")
print(f"  - benefits_category: {df['benefits_category'].value_counts().to_dict()}")

# Save enhanced main table
output_file = 'dashboard_main_table.xlsx'
df.to_excel(output_file, index=False)
print(f"\n✓ Saved enhanced table: {output_file}")

# ============================================================================
# 2. SKILLS TABLE - Split and normalize skills
# ============================================================================
print("\n" + "=" * 80)
print("CREATING SKILLS TABLE")
print("=" * 80)

skills_data = []

for idx, row in df.iterrows():
    job_id = row['job_id']
    skills_str = row['required_skills']
    
    if pd.notna(skills_str):
        skills = [s.strip() for s in str(skills_str).split(',')]
        for skill in skills:
            skills_data.append({
                'job_id': job_id,
                'skill': skill,
                'job_title': row['job_title'],
                'salary_usd': row['salary_usd'],
                'experience_level': row['experience_level'],
                'industry': row['industry'],
                'company_size': row['company_size']
            })

skills_df = pd.DataFrame(skills_data)
print(f"✓ Created skills table with {len(skills_df)} skill-job associations")
print(f"✓ Unique skills: {skills_df['skill'].nunique()}")
print(f"\nTop 10 skills:")
print(skills_df['skill'].value_counts().head(10))

# Save skills table
skills_output = 'dashboard_skills_table.xlsx'
skills_df.to_excel(skills_output, index=False)
print(f"\n✓ Saved skills table: {skills_output}")

# ============================================================================
# 3. AGGREGATED TABLES FOR QUICK REFERENCE
# ============================================================================
print("\n" + "=" * 80)
print("CREATING AGGREGATED SUMMARY TABLES")
print("=" * 80)

# Create Excel writer for multiple sheets
summary_file = 'dashboard_summary_tables.xlsx'
with pd.ExcelWriter(summary_file, engine='openpyxl') as writer:
    
    # Page 1 summaries
    jobs_by_month = df.groupby('posting_year_month').agg({
        'job_id': 'count',
        'salary_usd': 'mean'
    }).reset_index()
    jobs_by_month.columns = ['year_month', 'job_count', 'avg_salary']
    jobs_by_month.to_excel(writer, sheet_name='Jobs_Over_Time', index=False)
    
    jobs_by_role = df.groupby('job_title').agg({
        'job_id': 'count',
        'salary_usd': 'mean'
    }).reset_index().sort_values('job_id', ascending=False)
    jobs_by_role.columns = ['job_title', 'job_count', 'avg_salary']
    jobs_by_role.to_excel(writer, sheet_name='Jobs_By_Role', index=False)
    
    jobs_by_industry = df.groupby('industry').agg({
        'job_id': 'count',
        'salary_usd': 'mean'
    }).reset_index().sort_values('job_id', ascending=False)
    jobs_by_industry.columns = ['industry', 'job_count', 'avg_salary']
    jobs_by_industry.to_excel(writer, sheet_name='Jobs_By_Industry', index=False)
    
    # Page 2 summaries
    salary_by_experience = df.groupby('experience_level_full').agg({
        'salary_usd': ['mean', 'median', 'min', 'max', 'count']
    }).reset_index()
    salary_by_experience.columns = ['experience_level', 'avg_salary', 'median_salary', 
                                     'min_salary', 'max_salary', 'job_count']
    salary_by_experience.to_excel(writer, sheet_name='Salary_By_Experience', index=False)
    
    salary_by_remote = df.groupby('remote_category').agg({
        'salary_usd': ['mean', 'median', 'count']
    }).reset_index()
    salary_by_remote.columns = ['remote_category', 'avg_salary', 'median_salary', 'job_count']
    salary_by_remote.to_excel(writer, sheet_name='Salary_By_Remote', index=False)
    
    # Page 3 summaries
    top_skills = skills_df.groupby('skill').agg({
        'job_id': 'count',
        'salary_usd': 'mean'
    }).reset_index().sort_values('job_id', ascending=False)
    top_skills.columns = ['skill', 'job_count', 'avg_salary']
    top_skills.to_excel(writer, sheet_name='Top_Skills', index=False)
    
    benefits_by_employment = df.groupby('employment_type').agg({
        'benefits_score': 'mean',
        'job_id': 'count'
    }).reset_index().sort_values('benefits_score', ascending=False)
    benefits_by_employment.columns = ['employment_type', 'avg_benefits_score', 'job_count']
    benefits_by_employment.to_excel(writer, sheet_name='Benefits_By_Employment', index=False)
    
    # KPIs summary
    kpis = pd.DataFrame({
        'KPI': [
            'Total Jobs',
            'Active Jobs',
            'Average Salary (USD)',
            'Median Salary (USD)',
            'Min Salary (USD)',
            'Max Salary (USD)',
            'Remote Jobs %',
            'Avg Years Experience',
            'Avg Benefits Score',
            'Unique Job Titles',
            'Unique Industries',
            'Unique Skills'
        ],
        'Value': [
            len(df),
            df['is_active'].sum(),
            f"${df['salary_usd'].mean():,.2f}",
            f"${df['salary_usd'].median():,.2f}",
            f"${df['salary_usd'].min():,}",
            f"${df['salary_usd'].max():,}",
            f"{(df['remote_ratio'] > 0).sum() / len(df) * 100:.1f}%",
            f"{df['years_experience'].mean():.1f}",
            f"{df['benefits_score'].mean():.2f}",
            df['job_title'].nunique(),
            df['industry'].nunique(),
            skills_df['skill'].nunique()
        ]
    })
    kpis.to_excel(writer, sheet_name='KPIs', index=False)

print(f"✓ Created summary tables with multiple sheets:")
print(f"  - Jobs_Over_Time: {len(jobs_by_month)} months")
print(f"  - Jobs_By_Role: {len(jobs_by_role)} roles")
print(f"  - Jobs_By_Industry: {len(jobs_by_industry)} industries")
print(f"  - Salary_By_Experience: {len(salary_by_experience)} levels")
print(f"  - Top_Skills: {len(top_skills)} skills")
print(f"  - KPIs: 12 key metrics")
print(f"\n✓ Saved: {summary_file}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("DATA PREPARATION COMPLETE!")
print("=" * 80)
print("\n📁 FILES CREATED:")
print(f"  1. {output_file} - Main table with calculated columns")
print(f"  2. {skills_output} - Normalized skills table")
print(f"  3. {summary_file} - Pre-aggregated summary tables")

print("\n📊 HOW TO USE THESE FILES:")
print("\n  For Power BI / Tableau:")
print("    - Import all 3 Excel files")
print("    - Use dashboard_main_table.xlsx as your fact table")
print("    - Join dashboard_skills_table.xlsx for skill analysis")
print("    - Use dashboard_summary_tables.xlsx for quick visuals")
print()
print("  For Python (Plotly/Dash/Streamlit):")
print("    - Read the files with pandas")
print("    - Use the pre-calculated columns for filtering")
print("    - Create interactive visualizations")
print()
print("  For Excel:")
print("    - Open dashboard_summary_tables.xlsx")
print("    - Each sheet is ready for pivot tables and charts")
print("    - Use slicers for interactive filters")

print("\n✅ You now have everything needed to build the 3-page dashboard!")
print("=" * 80)
