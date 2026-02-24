import pandas as pd

def load_raw_data():
    """Load all 3 raw CSV files."""
    users = pd.read_csv("data/raw/EduPro Online Platform.xlsx - Users.csv")
    courses = pd.read_csv("data/raw/EduPro Online Platform.xlsx - Courses.csv")
    transactions = pd.read_csv("data/raw/EduPro Online Platform.xlsx - Transactions.csv")
    return users, courses, transactions

def add_age_group(df):
    """Add AgeGroup column based on Age."""
    bins = [0, 17, 25, 35, 45, 100]
    labels = ["<18", "18–25", "26–35", "36–45", "45+"]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)
    return df

def merge_data(users, courses, transactions):
    """Join users + transactions + courses into one master table."""
    df = transactions.merge(users, on="UserID").merge(courses, on="CourseID")
    df = add_age_group(df)
    return df

def load_clean_data(path="data/processed/edupro_clean_data.csv"):
    """Load the pre-processed merged CSV."""
    df = pd.read_csv(path)
    return df

def build_and_save_clean_data():
    """Run once to generate the clean merged file."""
    users, courses, transactions = load_raw_data()
    df = merge_data(users, courses, transactions)
    df.to_csv("data/processed/edupro_clean_data.csv", index=False)
    print(f"✅ Saved clean data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df