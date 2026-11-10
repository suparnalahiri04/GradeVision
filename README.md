# 🎓 GradeVision
### Student Performance Analytics & Academic Insights

**GradeVision** is a Python-based academic analytics dashboard that helps analyse student performance, evaluate academic results, and generate meaningful insights through interactive visualisations.

Built using Streamlit, Pandas, and Plotly, the application allows users to upload student datasets, automatically identify subject columns, calculate grades, analyse class performance, and generate individual student reports.

**GitHub Repository:** [suparnalahiri04/GradeVision](https://github.com/suparnalahiri04/GradeVision)

## 📸 Dashboard Preview

### 1. Dashboard Overview
![Dashboard Overview](assets/dashboard-overview.png)

### 2. Performance Analytics
![Performance Analytics](assets/performance-analytics.png)

### 3. Student Leaderboard
![Student Leaderboard](assets/student-leaderboard.png)

## ✨ Key Features

- **CSV Dataset Upload:** Upload custom student datasets for analysis.
- **Dynamic Subject Detection:** Automatically identify numeric subject columns.
- **Automated Grade Calculation:** Calculate student grades using the configured grading scale.
- **Academic Overview:** Display total students, class average, highest student average, and pass percentage.
- **Subject Performance Analysis:** Visualise average marks across subjects.
- **Grade Distribution:** Explore grade distribution through interactive charts.
- **Student Leaderboard:** Rank students based on academic performance.
- **Individual Student Reports:** View subject-wise marks, average, grade, and class rank.
- **CSV Export:** Download processed student analytics reports.
- **Input Validation:** Validate student names, numeric marks, and score ranges.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Data Processing | Pandas |
| Data Visualisation | Plotly |
| Testing | Pytest |
| Dataset Format | CSV |
| Development Environment | VS Code |

## 📊 Grading System

| Grade | Marks Range |
|---|---:|
| A+ | 93–100 |
| A | 85–92 |
| B+ | 77–84 |
| B | 69–76 |
| C+ | 61–68 |
| C | 53–60 |
| D | 45–52 |
| F | Below 45 |

Students with an average of at least 45% are considered to have passed.

## 📁 Project Structure

```text
GradeVision/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── dashboard-overview.png
│   ├── performance-analytics.png
│   └── student-leaderboard.png
│
├── data/
│   └── sample_students.csv
│
├── tests/
│   └── test_analytics.py
│
├── app.py
├── analytics.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/suparnalahiri04/GradeVision.git
cd GradeVision
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🧪 Running Tests

Execute the automated test suite:

```bash
python -m pytest tests/ -v
```

Tests cover grade calculation, subject detection, input validation, student analysis, and academic statistics.

## 📄 Dataset Format

GradeVision accepts CSV files containing a student name column and one or more numeric subject columns.

Example:

```csv
Name,Math,Science,English,Computer
Aarav Sharma,95,92,97,99
Ananya Verma,88,91,86,90
Rohan Mehta,78,82,75,80
Isha Kapoor,84,79,88,81
```

**Dataset requirements:**
- A `Name` column is required.
- At least one numeric subject column is required.
- Subject marks must be between 0 and 100.
- Student names and marks must not be empty.

## 🚀 Future Enhancements

- Predictive student performance analysis using Machine Learning.
- Identification of students requiring academic support.
- Attendance and assignment performance integration.
- Semester-wise performance tracking.
- Automated academic report generation in PDF format.
- Role-based dashboards for students, teachers, and administrators.

## 🎯 Project Objective

GradeVision aims to simplify academic performance monitoring by transforming raw student marks into meaningful visual insights, helping educators identify performance patterns and make data-driven academic decisions.

## 👩‍💻 Project

**GradeVision – Student Performance Analytics & Academic Insights**

Developed using Python, Streamlit, Pandas, and Plotly.

**Repository:** https://github.com/suparnalahiri04/GradeVision

