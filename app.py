# ==============================
# STREAMLIT DASHBOARD
# ==============================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# LOAD DATA
# ------------------------------
df = pd.read_csv("responses.csv")
answers = pd.read_csv("answers.csv")

# ------------------------------
# CREATE ANSWER KEY
# ------------------------------
answer_key = dict(zip(answers["Question"], answers["Answer"]))

# ------------------------------
# CALCULATE SCORE
# ------------------------------
def calculate_score(row):
    score = 0
    for q in answer_key:
        if row[q] == answer_key[q]:
            score += 1
    return score

df["Score"] = df.apply(calculate_score, axis=1)

# ------------------------------
# TITLE
# ------------------------------
st.title("📊 MCQ Quiz Analytics Dashboard")

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("Filters")

selected_college = st.sidebar.selectbox(
    "Select College", ["All"] + list(df["College"].unique())
)

selected_dept = st.sidebar.selectbox(
    "Select Department", ["All"] + list(df["Department"].unique())
)

# Apply filters
filtered_df = df.copy()

if selected_college != "All":
    filtered_df = filtered_df[filtered_df["College"] == selected_college]

if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Department"] == selected_dept]

# ------------------------------
# SHOW DATA
# ------------------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)

# ------------------------------
# SCORE DISTRIBUTION
# ------------------------------
st.subheader("📊 Score Distribution")

fig, ax = plt.subplots()
sns.histplot(filtered_df["Score"], bins=5, ax=ax)
ax.set_title("Score Distribution")

st.pyplot(fig)

# ------------------------------
# TOP STUDENTS
# ------------------------------
st.subheader("🏆 Top Students")

top_students = filtered_df.sort_values("Score", ascending=False)
st.dataframe(top_students[["Name", "Score"]].head(10))

# ------------------------------
# DEPARTMENT PERFORMANCE
# ------------------------------
st.subheader("🏢 Department Performance")

dept_perf = filtered_df.groupby("Department")["Score"].mean()

fig2, ax2 = plt.subplots()
dept_perf.plot(kind="bar", ax=ax2)
ax2.set_title("Department Performance")

st.pyplot(fig2)

# ------------------------------
# COLLEGE PERFORMANCE
# ------------------------------
st.subheader("🏫 College Performance")

college_perf = filtered_df.groupby("College")["Score"].mean()

fig3, ax3 = plt.subplots()
college_perf.plot(kind="barh", ax=ax3)
ax3.set_title("College Performance")

st.pyplot(fig3)

# ------------------------------
# QUESTION ANALYSIS
# ------------------------------
st.subheader("❓ Question Analysis")

question_accuracy = {}

for q in answer_key:
    correct = (filtered_df[q] == answer_key[q]).sum()
    question_accuracy[q] = correct / len(filtered_df)

question_df = pd.DataFrame.from_dict(
    question_accuracy, orient="index", columns=["Accuracy"]
)

st.dataframe(question_df)

fig4, ax4 = plt.subplots()
question_df.plot(kind="bar", ax=ax4)
ax4.set_title("Question Accuracy")

st.pyplot(fig4)