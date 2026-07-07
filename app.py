import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Instructor Performance & Course Quality Evaluation")
st.markdown("---")

# -----------------------------------
# Load Dataset
# -----------------------------------
@st.cache_data
def load_data():

    teachers = pd.read_excel(
        "EduPro Online Platform.xlsx",
        sheet_name="Teachers"
    )

    courses = pd.read_excel(
        "EduPro Online Platform.xlsx",
        sheet_name="Courses"
    )

    transactions = pd.read_excel(
        "EduPro Online Platform.xlsx",
        sheet_name="Transactions"
    )

    users = pd.read_excel(
        "EduPro Online Platform.xlsx",
        sheet_name="Users"
    )

    df = transactions.merge(teachers,on="TeacherID")
    df = df.merge(courses,on="CourseID")
    df = df.merge(users,on="UserID")

    return df

df = load_data()

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Filters")

expertise = st.sidebar.multiselect(
    "Expertise",
    sorted(df["Expertise"].unique()),
    default=sorted(df["Expertise"].unique())
)

category = st.sidebar.multiselect(
    "Course Category",
    sorted(df["CourseCategory"].unique()),
    default=sorted(df["CourseCategory"].unique())
)

level = st.sidebar.multiselect(
    "Course Level",
    sorted(df["CourseLevel"].unique()),
    default=sorted(df["CourseLevel"].unique())
)

filtered_df = df[
    (df["Expertise"].isin(expertise)) &
    (df["CourseCategory"].isin(category)) &
    (df["CourseLevel"].isin(level))
]

# -----------------------------------
# KPI Cards
# -----------------------------------
st.subheader("Dashboard KPIs")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Teachers",
    filtered_df["TeacherID"].nunique()
)

c2.metric(
    "Courses",
    filtered_df["CourseID"].nunique()
)

c3.metric(
    "Students",
    filtered_df["UserID"].nunique()
)

c4.metric(
    "Enrollments",
    len(filtered_df)
)

c5,c6 = st.columns(2)

c5.metric(
    "Average Teacher Rating",
    round(filtered_df["TeacherRating"].mean(),2)
)

c6.metric(
    "Average Course Rating",
    round(filtered_df["CourseRating"].mean(),2)
)

st.divider()

# -----------------------------------
# Scatter Plot
# -----------------------------------
st.subheader("Experience vs Teacher Rating")

fig = px.scatter(
    filtered_df,
    x="YearsOfExperience",
    y="TeacherRating",
    color="Expertise",
    hover_name="TeacherName",
    trendline="ols"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Top Teachers
# -----------------------------------
st.subheader("Top 10 Teachers")

leaderboard = (
    filtered_df.groupby("TeacherName")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    leaderboard,
    x="TeacherName",
    y="TeacherRating",
    color="TeacherRating",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Course Category Ratings
# -----------------------------------
st.subheader("Average Course Rating by Category")

category_rating = (
    filtered_df.groupby("CourseCategory")["CourseRating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    category_rating,
    x="CourseCategory",
    y="CourseRating",
    color="CourseRating",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Expertise Performance
# -----------------------------------
st.subheader("Teacher Rating by Expertise")

exp = (
    filtered_df.groupby("Expertise")["TeacherRating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    exp,
    x="Expertise",
    y="TeacherRating",
    color="TeacherRating",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Enrollment by Teacher
# -----------------------------------
st.subheader("Enrollment by Teacher")

enrollment = (
    filtered_df.groupby("TeacherName")
    .size()
    .reset_index(name="Enrollments")
)

fig = px.bar(
    enrollment,
    x="TeacherName",
    y="Enrollments",
    color="Enrollments"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Heatmap
# -----------------------------------
st.subheader("Course Rating Heatmap")

pivot = filtered_df.pivot_table(
    values="CourseRating",
    index="CourseCategory",
    columns="CourseLevel",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    pivot,
    annot=True,
    cmap="YlGnBu",
    ax=ax
)

st.pyplot(fig)

# -----------------------------------
# Pie Chart
# -----------------------------------
st.subheader("Course Level Distribution")

fig = px.pie(
    filtered_df,
    names="CourseLevel"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Top Courses
# -----------------------------------
st.subheader("Top Rated Courses")

top_courses = (
    filtered_df.groupby("CourseName")["CourseRating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_courses)

# -----------------------------------
# Download Data
# -----------------------------------
st.subheader("Download Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    "Filtered_Data.csv",
    "text/csv"
)