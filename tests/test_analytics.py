
import pandas as pd
import pytest

from analytics import (
    SUBJECTS,
    calculate_grade,
    detect_subject_columns,
    analyze_students,
    get_class_statistics,
    get_grade_distribution
)


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Math": [95, 80, 40],
        "Science": [90, 85, 40],
        "English": [96, 75, 40],
        "Computer": [99, 80, 40]
    })


@pytest.fixture
def analyzed_data(sample_data):
    return analyze_students(sample_data)


# =====================================================
# GRADE CALCULATION TESTS
# =====================================================

@pytest.mark.parametrize(
    "marks, expected",
    [
        (100, "A+"),
        (93, "A+"),
        (92, "A"),
        (85, "A"),
        (84, "B+"),
        (77, "B+"),
        (76, "B"),
        (69, "B"),
        (68, "C+"),
        (61, "C+"),
        (60, "C"),
        (53, "C"),
        (52, "D"),
        (45, "D"),
        (44, "F"),
        (0, "F")
    ]
)
def test_calculate_grade(marks, expected):
    assert calculate_grade(marks) == expected


# =====================================================
# SUBJECT DETECTION TESTS
# =====================================================

def test_detect_default_subjects(sample_data):
    assert detect_subject_columns(sample_data) == SUBJECTS


def test_detect_custom_subjects():
    data = pd.DataFrame({
        "Name": ["A", "B"],
        "Student ID": [101, 102],
        "Physics": [80, 90],
        "Chemistry": [75, 85],
        "Biology": [88, 92]
    })

    assert detect_subject_columns(data) == [
        "Physics",
        "Chemistry",
        "Biology"
    ]


def test_exclude_identifier_columns():
    data = pd.DataFrame({
        "Name": ["A", "B"],
        "Roll Number": [1, 2],
        "Age": [20, 21],
        "Math": [90, 80]
    })

    assert detect_subject_columns(data) == ["Math"]


def test_no_numeric_subjects():
    data = pd.DataFrame({
        "Name": ["A", "B"],
        "Class": ["X", "XI"]
    })

    with pytest.raises(ValueError):
        detect_subject_columns(data)


# =====================================================
# STUDENT ANALYSIS TESTS
# =====================================================

def test_analyze_students(analyzed_data):
    assert len(analyzed_data) == 3
    assert "Total" in analyzed_data.columns
    assert "Average" in analyzed_data.columns
    assert "Grade" in analyzed_data.columns
    assert "Result" in analyzed_data.columns
    assert "Rank" in analyzed_data.columns


def test_total_and_average(analyzed_data):
    alice = analyzed_data[
        analyzed_data["Name"] == "Alice"
    ].iloc[0]

    assert alice["Total"] == 380
    assert alice["Average"] == 95.0


def test_student_grades(analyzed_data):
    grades = dict(
        zip(
            analyzed_data["Name"],
            analyzed_data["Grade"]
        )
    )

    assert grades["Alice"] == "A+"
    assert grades["Bob"] == "B+"
    assert grades["Charlie"] == "F"


def test_student_results(analyzed_data):
    results = dict(
        zip(
            analyzed_data["Name"],
            analyzed_data["Result"]
        )
    )

    assert results["Alice"] == "Pass"
    assert results["Bob"] == "Pass"
    assert results["Charlie"] == "Fail"


def test_student_ranking(analyzed_data):
    ranks = dict(
        zip(
            analyzed_data["Name"],
            analyzed_data["Rank"]
        )
    )

    assert ranks["Alice"] == 1
    assert ranks["Bob"] == 2
    assert ranks["Charlie"] == 3


def test_tied_student_ranks():
    data = pd.DataFrame({
        "Name": ["A", "B", "C"],
        "Math": [90, 90, 80],
        "Science": [90, 90, 80],
        "English": [90, 90, 80],
        "Computer": [90, 90, 80]
    })

    result = analyze_students(data)

    ranks = dict(zip(result["Name"], result["Rank"]))

    assert ranks["A"] == 1
    assert ranks["B"] == 1
    assert ranks["C"] == 3


def test_custom_subject_analysis():
    data = pd.DataFrame({
        "Name": ["A", "B"],
        "Student ID": [101, 102],
        "Physics": [90, 80],
        "Chemistry": [80, 70]
    })

    result = analyze_students(data)

    assert result.loc[0, "Total"] == 170
    assert result.loc[0, "Average"] == 85
    assert "Student ID" not in result.columns


# =====================================================
# CLASS STATISTICS TESTS
# =====================================================

def test_class_statistics(analyzed_data):
    stats = get_class_statistics(analyzed_data)

    assert stats["total_students"] == 3
    assert stats["class_average"] == 71.67
    assert stats["highest_average"] == 95.0
    assert stats["lowest_average"] == 40.0
    assert stats["pass_percentage"] == 66.67
    assert stats["topper"] == "Alice"


def test_grade_distribution(analyzed_data):
    distribution = get_grade_distribution(analyzed_data)

    assert distribution["A+"] == 1
    assert distribution["B+"] == 1
    assert distribution["F"] == 1
    assert distribution["A"] == 0


# =====================================================
# VALIDATION TESTS
# =====================================================

def test_missing_name_column():
    data = pd.DataFrame({
        "Math": [90],
        "Science": [80]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


def test_missing_subject_column():
    data = pd.DataFrame({
        "Name": ["A"],
        "Math": [90]
    })

    with pytest.raises(ValueError):
        analyze_students(
            data,
            subject_columns=["Math", "Science"]
        )


def test_empty_dataset():
    data = pd.DataFrame(
        columns=["Name", "Math"]
    )

    with pytest.raises(ValueError):
        analyze_students(data)


def test_empty_names():
    data = pd.DataFrame({
        "Name": ["", "A"],
        "Math": [90, 80]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


def test_missing_marks():
    data = pd.DataFrame({
        "Name": ["A"],
        "Math": [None]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


def test_non_numeric_marks():
    data = pd.DataFrame({
        "Name": ["A"],
        "Math": ["Excellent"]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


@pytest.mark.parametrize("invalid_mark", [-1, 101])
def test_marks_outside_range(invalid_mark):
    data = pd.DataFrame({
        "Name": ["A"],
        "Math": [invalid_mark]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


def test_name_cleaning():
    data = pd.DataFrame({
        "Name": ["  Alice  "],
        "Math": [90]
    })

    result = analyze_students(data)

    assert result.iloc[0]["Name"] == "Alice"


def test_empty_name_with_nan():
    data = pd.DataFrame({
        "Name": [None],
        "Math": [90]
    })

    with pytest.raises(ValueError):
        analyze_students(data)


def test_duplicate_student_names():
    data = pd.DataFrame({
        "Name": ["Alex", "Alex"],
        "Math": [90, 80]
    })

    result = analyze_students(data)

    assert len(result) == 2


def test_statistics_empty_dataframe():
    data = pd.DataFrame({
        "Average": [],
        "Total": [],
        "Result": [],
        "Name": []
    })

    with pytest.raises(ValueError):
        get_class_statistics(data)
