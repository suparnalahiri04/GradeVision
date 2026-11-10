
import pandas as pd

# Default subjects for the sample dataset
SUBJECTS = ["Math", "Science", "English", "Computer"]

GRADING_SCALE = [
    (93, "A+"),
    (85, "A"),
    (77, "B+"),
    (69, "B"),
    (61, "C+"),
    (53, "C"),
    (45, "D"),
    (0, "F")
]

# Numeric columns that should never be treated as subjects
EXCLUDED_COLUMNS = {
    "id",
    "student id",
    "roll number",
    "roll no",
    "roll_no",
    "age",
    "phone",
    "mobile",
    "contact",
    "year",
    "semester"
}


def calculate_grade(average):
    for threshold, grade in GRADING_SCALE:
        if average >= threshold:
            return grade
    return "F"


def detect_subject_columns(df):
    """
    Detect numeric subject columns while excluding
    common student identifiers and metadata.
    """
    subject_columns = []

    for column in df.columns:
        normalized = str(column).strip().lower()

        if normalized in EXCLUDED_COLUMNS:
            continue

        # Exclude non-numeric columns
        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if numeric_values.notna().any():
            subject_columns.append(column)

    if not subject_columns:
        raise ValueError(
            "No numeric subject columns were found in the dataset."
        )

    return subject_columns


def analyze_students(df, subject_columns=None):
    """
    Validate student data and calculate academic results.
    Supports dynamically detected subject columns.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("The dataset contains no student records.")

    # Clean column names
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Check for student name column
    if "Name" not in df.columns:
        raise ValueError("Missing required column: Name")

    # Detect subjects if not explicitly supplied
    if subject_columns is None:
        subject_columns = detect_subject_columns(df)

    if not subject_columns:
        raise ValueError("At least one subject column is required.")

    missing = [
        col for col in subject_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing subject columns: {missing}")

    if "Name" in subject_columns:
        raise ValueError("Name cannot be treated as a subject.")

    result = df[["Name"] + subject_columns].copy()

    # Validate names
    result["Name"] = result["Name"].astype("string").str.strip()

    if result["Name"].isna().any() or (result["Name"] == "").any():
        raise ValueError("Student names cannot be empty.")

    # Convert subject marks to numeric
    for subject in subject_columns:
        result[subject] = pd.to_numeric(
            result[subject],
            errors="coerce"
        )

    # Validate missing or non-numeric marks
    if result[subject_columns].isna().any().any():
        raise ValueError(
            "All subject marks must be numeric and non-empty."
        )

    # Validate mark range
    if (
        (result[subject_columns] < 0) |
        (result[subject_columns] > 100)
    ).any().any():

        raise ValueError(
            "Marks must be between 0 and 100."
        )

    # Academic calculations
    result["Total"] = result[subject_columns].sum(axis=1)

    result["Average"] = (
        result[subject_columns]
        .mean(axis=1)
        .round(2)
    )

    result["Grade"] = result["Average"].apply(calculate_grade)

    result["Result"] = result["Average"].apply(
        lambda x: "Pass" if x >= 45 else "Fail"
    )

    result["Rank"] = (
        result["Total"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    # Sort students by rank
    result = result.sort_values(
        ["Rank", "Name"]
    ).reset_index(drop=True)

    # Store detected subjects for downstream use
    result.attrs["subject_columns"] = list(subject_columns)

    return result


def get_class_statistics(df):
    if df.empty:
        raise ValueError("Cannot calculate statistics for an empty dataset.")

    return {
        "total_students": len(df),
        "class_average": round(df["Average"].mean(), 2),
        "highest_average": round(df["Average"].max(), 2),
        "lowest_average": round(df["Average"].min(), 2),
        "pass_percentage": round(
            (df["Result"] == "Pass").mean() * 100,
            2
        ),
        "topper": df.loc[df["Total"].idxmax(), "Name"]
    }


def get_grade_distribution(df):
    grade_order = [
        "A+", "A", "B+", "B",
        "C+", "C", "D", "F"
    ]

    return (
        df["Grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
    )
