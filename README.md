# AI Job Market Analysis - South Korea

Data analysis and dashboard preparation for AI job market in South Korea.

## 📋 Prerequisites

- Python 3.8 or higher
- Git

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd ai_job
```

### 2. Create a virtual environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify installation
```bash
python -c "import pandas; import openpyxl; print('✓ All dependencies installed!')"
```

## 📁 Project Structure

```
ai_job/
├── dataset/
│   └── ai_job_dataset.xlsx          # Original dataset
├── script/
│   ├── filter.py                    # Filter jobs by country
│   ├── dashboard_analysis.py        # Analyze data for dashboard insights
│   └── prepare_dashboard_data.py    # Prepare data for visualization
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🛠️ Usage

### Filter data by country
```bash
cd script
python filter.py
```
This creates `south_korea_jobs.xlsx` with filtered results.

### Analyze dashboard insights
```bash
cd script
python dashboard_analysis.py
```
Shows what KPIs and visuals are available from the data.

### Prepare dashboard data
```bash
cd script
python prepare_dashboard_data.py
```
Creates three files:
- `dashboard_main_table.xlsx` - Enhanced data with calculated columns
- `dashboard_skills_table.xlsx` - Normalized skills data
- `dashboard_summary_tables.xlsx` - Pre-aggregated summaries

## 📊 Dashboard Pages

The project prepares data for a 3-page dashboard:

1. **Executive Overview** - Market snapshot with KPIs and trends
2. **Salary & Experience Insights** - Compensation analysis
3. **Skills & Job Quality** - In-demand skills and benefits

## 🤝 Contributing

1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Commit and push
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

4. Create a Pull Request

## 📝 Notes

- The virtual environment folder (`venv/`, `bin/`, `lib/`) is ignored by git
- Generated output files (`.xlsx` in script/) are also ignored
- Only source code and the original dataset are tracked

## 💡 Need Help?

If you encounter any issues:
1. Make sure your virtual environment is activated
2. Verify Python version: `python --version`
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
