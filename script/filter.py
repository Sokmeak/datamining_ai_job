import pandas as pd

# 1. Load the dataset
input_file = "../dataset/ai_job_dataset.xlsx"   # change this if your file name is different

if(not input_file.endswith('.xlsx')):
    raise ValueError("Input file must be an .xlsx file" )


df = pd.read_excel(input_file)

# 2. Filter rows where employee_residence = "South Korea"
filtered_df = df[df["employee_residence"] == "South Korea"]
print("Number of jobs in South Korea:", len(filtered_df))

# 3. Save to a new .xlsx file
output_file = "south_korea_jobs.xlsx"
filtered_df.to_excel(output_file, index=False)

print("Filtered file saved as:", output_file)
