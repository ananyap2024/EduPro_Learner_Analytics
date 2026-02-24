# EduPro Learner Demographics and Enrollment Analytics

## Project Overview
This project analyzes learner demographics and course enrollment behavior on the EduPro platform. The objective is to understand how different demographic segments interact with courses and to extract actionable insights using data analysis, KPI computation, and an interactive Streamlit dashboard.

The project follows a modular analytics architecture with a clear separation between data processing, KPI logic, and visualization.

---

## Objectives
The project aims to answer the following questions:
- What is the age distribution of learners on EduPro?
- How does course enrollment vary across age groups?
- Are there gender-based differences in course selection?
- Which course categories attract the highest enrollments?
- Do beginners prefer certain course types or levels?

---

## Project Architecture
The project is structured into three layers:
1. Data Analysis Layer – Data cleaning, integration, and exploratory analysis
2. KPI Layer – Business metric computation using reusable functions
3. Visualization Layer – Interactive dashboard built with Streamlit

---

## Folder Structure
learner_analytics/
│
├── data/
│   ├── raw/
│   │   └── EduPro_Data.xlsx
│   └── processed/
│       └── edupro_clean_data.csv
│
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   └── 02_kpi_analysis.ipynb
│
├── src/
│   ├── data_processing.py
│   ├── kpi_calculations.py
│   └── utils.py
│
├── streamlit_app/
│   └── app.py
│
├── outputs/
│   ├── figures/
│   └── reports/
│
├── requirements.txt
├── .gitignore
└── README.md

---

## Dataset Description

Users Sheet:
- UserID
- UserName
- Age
- Gender

Teachers Sheet:
- TeacherID
- TeacherName
- Age
- Gender
- Expertise
- YearsOfExperience
- TeacherRating

Courses Sheet:
- CourseID
- CourseName
- CourseCategory
- CourseType
- CourseLevel

Transactions Sheet:
- TransactionID
- UserID
- CourseID
- TransactionDate

---

## Key Performance Indicators (KPIs)

- Total Enrollments: Overall platform engagement
- Enrollments by Age Group: Demographic reach
- Gender Participation Ratio: Inclusivity metric
- Category Popularity Index: Course demand indicator
- Level Preference Distribution: Skill maturity insight

---

## Streamlit Dashboard Features

Core Modules:
- Learner demographic overview
- Age-wise enrollment analysis
- Gender-based course preference analysis
- Course category popularity visualization

User Controls:
- Age group filters
- Gender filters
- Course category selection
- Course level selection

---

## Technologies Used
- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Streamlit
- Git & GitHub
- VS Code

---

## How to Run the Project Locally

1. Clone the Repository
git clone https://github.com/your-username/learner-analytics.git
cd learner_analytics

2. Create and Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate   (Windows)

3. Install Dependencies
pip install -r requirements.txt

4. Run the Streamlit App
cd streamlit_app
streamlit run app.py

---

## Notes
- The .venv folder is intentionally excluded from version control.
- All cleaned and processed data is stored in data/processed/.
- KPI logic is centralized in src/kpi_calculations.py for reuse.

---

## Future Enhancements
- Time-based enrollment trend analysis
- Learner segmentation using clustering
- Exportable dashboard reports
- Cloud deployment

---

## Author
Ananya  
Aspiring Data Analyst