def total_enrollments(df):
    return df.shape[0]

def top_age_group(df):
    return df["AgeGroup"].value_counts().idxmax()

def dominant_gender(df):
    return df["Gender"].value_counts().idxmax()

def top_category(df):
    return df["CourseCategory"].value_counts().idxmax()

def top_level(df):
    return df["CourseLevel"].value_counts().idxmax()

def enrollments_by_age(df):
    return df.groupby("AgeGroup", observed=True)["CourseID"].count().reset_index()

def gender_participation(df):
    return df["Gender"].value_counts(normalize=True).mul(100).round(1)

def category_popularity(df):
    return df["CourseCategory"].value_counts().reset_index()

def level_distribution(df):
    return df["CourseLevel"].value_counts(normalize=True).mul(100).round(1).reset_index()

def age_category_heatmap_data(df):
    return df.pivot_table(index="AgeGroup", columns="CourseCategory",
                          values="CourseID", aggfunc="count", observed=True)

def gender_level_data(df):
    return df.pivot_table(index="Gender", columns="CourseLevel",
                          values="CourseID", aggfunc="count", observed=True)