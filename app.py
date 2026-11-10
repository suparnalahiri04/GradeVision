
import streamlit as st
import pandas as pd
import plotly.express as px

from analytics import (
    analyze_students,
    detect_subject_columns,
    get_class_statistics,
    get_grade_distribution
)


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="GradeVision | Academic Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. DESIGN COLORS
# =====================================================

COLORS = {
    "primary": "#4F46E5",
    "secondary": "#818CF8",
    "background": "#F1F5F9",
    "text": "#1E293B",
    "heading": "#172554",
    "border": "#CBD5E1"
}

SUBJECT_COLORS = [
    "#4F46E5",
    "#0891B2",
    "#7C3AED",
    "#0D9488",
    "#2563EB",
    "#9333EA",
    "#D97706",
    "#DB2777"
]

GRADE_COLORS = {
    "A+": "#059669",
    "A": "#34D399",
    "B+": "#2563EB",
    "B": "#60A5FA",
    "C+": "#F59E0B",
    "C": "#FBBF24",
    "D": "#F87171",
    "F": "#DC2626"
}


# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background-color: #F1F5F9 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3, h4 {
    color: #172554 !important;
    font-weight: 750 !important;
}

/* Captions */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    font-size: 13px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E2E8F0 !important;
    border-right: 1px solid #CBD5E1;
}

[data-testid="stSidebar"] * {
    color: #1E293B !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: #172554 !important;
    font-weight: 650 !important;
}

/* Hero banner */
.hero {
    background: linear-gradient(
        120deg,
        #312E81,
        #4F46E5,
        #818CF8
    );
    padding: 34px;
    border-radius: 18px;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(49,46,129,0.18);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 38px;
    margin: 0;
}

.hero p {
    color: #E0E7FF !important;
    font-size: 16px;
    margin-bottom: 0;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #CBD5E1;
    box-shadow: 0 4px 12px rgba(15,23,42,0.06);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #312E81 !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #F8FAFC !important;
    border: 2px dashed #6366F1 !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #1E293B !important;
}

[data-testid="stFileUploader"] button {
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #3730A3 !important;
}

/* Chart containers */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF !important;
    border-radius: 14px;
    padding: 10px;
    border: 1px solid #E2E8F0;
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    overflow: hidden;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #1E293B !important;
}

[data-baseweb="select"] * {
    color: #1E293B !important;
}

/* Download button */
.stDownloadButton button {
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px;
    font-weight: 650;
}

.stDownloadButton button:hover {
    background-color: #3730A3 !important;
}

hr {
    border-color: #CBD5E1 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. CHART THEME
# =====================================================

# IMPORTANT: No margin, xaxis or yaxis here.
# Individual charts define their own margins.

CHART_LAYOUT = {
    "template": "plotly_white",
    "font": {
        "family": "Arial, sans-serif",
        "color": "#1E293B",
        "size": 14
    },
    "paper_bgcolor": "#FFFFFF",
    "plot_bgcolor": "#FFFFFF",
    "title_font": {
        "size": 18,
        "color": "#172554"
    },
    "title_x": 0.5
}


def style_chart_axes(
    fig,
    x_title="Subjects",
    y_title="Marks",
    y_range=None
):
    fig.update_xaxes(
        title=x_title,
        title_font=dict(color="#172554", size=14),
        tickfont=dict(color="#1E293B", size=13),
        showline=True,
        linecolor="#64748B",
        linewidth=1.5,
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    fig.update_yaxes(
        title=y_title,
        title_font=dict(color="#172554", size=14),
        tickfont=dict(color="#1E293B", size=13),
        showline=True,
        linecolor="#64748B",
        linewidth=1.5,
        showgrid=True,
        gridcolor="#CBD5E1",
        gridwidth=1,
        zeroline=False,
        automargin=True,
        range=y_range
    )

    return fig


def style_dataframe(data):
    return (
        data.style
        .set_properties(**{
            "background-color": "#FFFFFF",
            "color": "#1E293B",
            "border-color": "#E2E8F0"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#E0E7FF"),
                    ("color", "#312E81"),
                    ("font-weight", "bold"),
                    ("border-color", "#CBD5E1")
                ]
            },
            {
                "selector": "tbody tr:nth-child(even)",
                "props": [
                    ("background-color", "#F8FAFC")
                ]
            }
        ])
    )


# =====================================================
# 5. HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>🎓 GradeVision</h1>
    <p>Student Performance Analytics & Academic Insights</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 GradeVision")
    st.caption("Academic Analytics Platform")

    st.divider()

    st.subheader("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload student marks CSV",
        type=["csv"]
    )

    st.caption(
        "Required: Name and at least one numeric subject column. "
        "Marks must be between 0 and 100."
    )

    st.divider()

    st.subheader("📊 College Grading Scale")

    grading = {
        "A+": "93–100",
        "A": "85–92",
        "B+": "77–84",
        "B": "69–76",
        "C+": "61–68",
        "C": "53–60",
        "D": "45–52",
        "F": "Below 45"
    }

    for grade, marks in grading.items():
        st.markdown(f"**{grade}** : {marks}")

    st.divider()

    st.caption("GradeVision | Academic Mini Project")


# =====================================================
# 7. LOAD AND ANALYZE DATA
# =====================================================

try:

    if uploaded_file is not None:
        raw_data = pd.read_csv(uploaded_file)
    else:
        raw_data = pd.read_csv("data/sample_students.csv")

    subject_cols = detect_subject_columns(raw_data)

    df = analyze_students(
        raw_data,
        subject_columns=subject_cols
    )

    if df.empty:
        st.error("The dataset contains no student records.")
        st.stop()

except Exception as e:

    st.error(f"Unable to process dataset: {e}")

    st.info(
        "Please upload a CSV with a Name column and "
        "at least one numeric subject column."
    )

    st.stop()


stats = get_class_statistics(df)
distribution = get_grade_distribution(df)


# =====================================================
# 8. ACADEMIC OVERVIEW
# =====================================================

st.subheader("📈 Academic Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Total Students",
    stats["total_students"]
)

c2.metric(
    "📊 Class Average",
    f'{stats["class_average"]:.2f}%'
)

c3.metric(
    "🏆 Top Student Average",
    f'{stats["highest_average"]:.2f}%'
)

c4.metric(
    "✅ Pass Percentage",
    f'{stats["pass_percentage"]:.2f}%'
)


# =====================================================
# 9. SUBJECT PERFORMANCE + GRADE DISTRIBUTION
# =====================================================

left, right = st.columns(2, gap="large")


# SUBJECT PERFORMANCE

with left:

    st.subheader("📚 Subject Performance")

    subject_avg = (
        df[subject_cols]
        .mean()
        .reset_index()
    )

    subject_avg.columns = [
        "Subject",
        "Average Marks"
    ]

    fig1 = px.bar(
        subject_avg,
        x="Subject",
        y="Average Marks",
        text_auto=".1f",
        color="Subject",
        color_discrete_sequence=SUBJECT_COLORS,
        title="Average Marks by Subject"
    )

    fig1.update_layout(
        **CHART_LAYOUT,
        margin=dict(l=60, r=25, t=65, b=60),
        showlegend=False
    )

    style_chart_axes(
        fig1,
        x_title="Subjects",
        y_title="Average Marks",
        y_range=[0, 105]
    )

    fig1.update_traces(
        textposition="outside",
        textfont=dict(
            color="#172554",
            size=13
        )
    )

    st.plotly_chart(
        fig1,
        width="stretch",
        config={"displayModeBar": False}
    )


# GRADE DISTRIBUTION

with right:

    st.subheader("🏅 Grade Distribution")

    grade_df = distribution.reset_index()
    grade_df.columns = ["Grade", "Students"]

    fig2 = px.pie(
        grade_df,
        names="Grade",
        values="Students",
        hole=0.5,
        color="Grade",
        color_discrete_map=GRADE_COLORS,
        title="Student Grade Breakdown"
    )

    # Margin is defined only once.
    fig2.update_layout(
        **CHART_LAYOUT,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(
            font=dict(
                color="#1E293B",
                size=12
            )
        )
    )

    fig2.update_traces(
        textposition="inside",
        textinfo="label+percent",
        textfont=dict(
            color="#FFFFFF",
            size=12
        ),
        marker=dict(
            line=dict(
                color="#FFFFFF",
                width=2
            )
        ),
        hovertemplate=(
            "<b>Grade: %{label}</b><br>"
            "Students: %{value}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig2,
        width="stretch",
        config={"displayModeBar": False}
    )


# =====================================================
# 10. GRADE SUMMARY
# =====================================================

st.divider()

st.subheader("📊 Grade-wise Student Summary")

summary = pd.DataFrame({
    "Grade": distribution.index,
    "Number of Students": distribution.values
})

st.dataframe(
    style_dataframe(summary),
    width="stretch",
    hide_index=True
)


# =====================================================
# 11. STUDENT LEADERBOARD
# =====================================================

st.divider()

st.subheader("🏆 Student Leaderboard")

st.caption(
    "Select a student row to view their individual academic report."
)

leaderboard = df[
    ["Rank", "Name"] + subject_cols +
    ["Total", "Average", "Grade", "Result"]
].copy().reset_index(drop=True)

leaderboard_event = st.dataframe(
    style_dataframe(leaderboard),
    width="stretch",
    hide_index=True,
    height=400,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "Rank": st.column_config.NumberColumn(
            "Rank",
            format="%d"
        ),
        "Total": st.column_config.NumberColumn(
            "Total Marks",
            format="%d"
        ),
        "Average": st.column_config.NumberColumn(
            "Average (%)",
            format="%.2f"
        )
    },
    key="student_leaderboard"
)


# =====================================================
# 12. INDIVIDUAL STUDENT REPORT
# =====================================================

st.divider()

st.subheader("👤 Individual Student Report")

selected_rows = leaderboard_event.selection.rows

student_names = df["Name"].tolist()

# Default student
default_student = df.iloc[0]["Name"]

# Get student selected from leaderboard
if selected_rows:

    selected_index = selected_rows[0]

    if 0 <= selected_index < len(leaderboard):
        default_student = leaderboard.iloc[selected_index]["Name"]

# Selectbox remembers the latest selected student.
if "individual_student_select" not in st.session_state:
    st.session_state.individual_student_select = default_student

# Sync leaderboard selection with selectbox.
if selected_rows:
    st.session_state.individual_student_select = default_student

selected_student = st.selectbox(
    "Select a student",
    student_names,
    key="individual_student_select"
)

student = df[
    df["Name"] == selected_student
].iloc[0]


a, b, c = st.columns(3)

a.metric(
    "📊 Average",
    f'{student["Average"]:.2f}%'
)

b.metric(
    "🎓 Grade",
    student["Grade"]
)

c.metric(
    "🏅 Class Rank",
    f'#{student["Rank"]}'
)


# Individual subject performance

student_scores = pd.DataFrame({
    "Subject": subject_cols,
    "Marks": [student[s] for s in subject_cols]
})

fig3 = px.bar(
    student_scores,
    x="Subject",
    y="Marks",
    color="Subject",
    color_discrete_sequence=SUBJECT_COLORS,
    text_auto=True,
    title=f"{selected_student} - Subject Performance"
)

fig3.update_layout(
    **CHART_LAYOUT,
    margin=dict(l=60, r=25, t=65, b=60),
    showlegend=False
)

style_chart_axes(
    fig3,
    x_title="Subjects",
    y_title="Marks",
    y_range=[0, 110]
)

fig3.update_traces(
    textposition="outside",
    textfont=dict(
        color="#172554",
        size=13
    )
)

st.plotly_chart(
    fig3,
    width="stretch",
    config={"displayModeBar": False}
)


# =====================================================
# 13. DOWNLOAD REPORT
# =====================================================

st.divider()

st.subheader("📥 Export Academic Report")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Student Analytics CSV",
    data=csv_data,
    file_name="GradeVision_Report.csv",
    mime="text/csv",
    type="primary"
)


# =====================================================
# 14. FOOTER
# =====================================================

st.markdown("""
<hr>

<div style="
    text-align:center;
    color:#475569;
    padding:15px;
    font-size:13px;
">
    🎓 <b>GradeVision</b><br>
    Student Performance Analytics Platform<br>
    Built using Python, Pandas, Streamlit and Plotly
</div>
""", unsafe_allow_html=True)
