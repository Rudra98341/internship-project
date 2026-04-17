# ==============================
# MCQ QUIZ ANALYTICS PROJECT
# ==============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# 1. LOAD DATA
# ------------------------------
df = pd.read_csv("responses.csv")
answers = pd.read_csv("answers.csv")

print("\n✅ Data Loaded Successfully\n")
print(df.head())

# ------------------------------
# 2. DATA PREPROCESSING
# ------------------------------
df.fillna("Not Answered", inplace=True)
df.columns = df.columns.str.strip()

# ------------------------------
# 3. CREATE ANSWER KEY
# ------------------------------
answer_key = dict(zip(answers["Question"], answers["Answer"]))
print("\n✅ Answer Key:\n", answer_key)

# ------------------------------
# 4. CALCULATE SCORE
# ------------------------------
def calculate_score(row):
    score = 0
    for q in answer_key:
        if row[q] == answer_key[q]:
            score += 1
    return score

df["Score"] = df.apply(calculate_score, axis=1)

print("\n✅ Scores Calculated\n")
print(df[["Name", "Score"]])

# ------------------------------
# 5. STUDENT ANALYSIS
# ------------------------------
print("\n🏆 TOP STUDENTS:\n")
top_students = df.sort_values("Score", ascending=False)
print(top_students[["Name", "Score"]])

print("\n📉 LOW PERFORMERS:\n")
low_students = df.sort_values("Score", ascending=True)
print(low_students[["Name", "Score"]].head())

# ------------------------------
# 6. BASIC INSIGHTS
# ------------------------------
print("\n📊 BASIC INSIGHTS:")
print("Average Score:", df["Score"].mean())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())

# ------------------------------
# 7. SCORE DISTRIBUTION
# ------------------------------
plt.figure()
sns.histplot(df["Score"], bins=5)
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()

# ------------------------------
# 8. DEPARTMENT ANALYSIS
# ------------------------------
dept_perf = df.groupby("Department")["Score"].mean()

print("\n🏢 Department Performance:\n")
print(dept_perf)

plt.figure()
dept_perf.plot(kind="bar")
plt.title("Department Performance")
plt.ylabel("Average Score")
plt.show()

# ------------------------------
# 9. COLLEGE ANALYSIS
# ------------------------------
college_perf = df.groupby("College")["Score"].mean()

print("\n🏫 College Performance:\n")
print(college_perf)

plt.figure()
college_perf.sort_values().plot(kind="barh")
plt.title("College Performance")
plt.xlabel("Average Score")
plt.show()

# ------------------------------
# 10. QUESTION ANALYSIS
# ------------------------------
question_accuracy = {}

for q in answer_key:
    correct = (df[q] == answer_key[q]).sum()
    question_accuracy[q] = correct / len(df)

question_df = pd.DataFrame.from_dict(
    question_accuracy, orient="index", columns=["Accuracy"]
)

print("\n❓ Question Analysis:\n")
print(question_df)

plt.figure()
question_df.plot(kind="bar")
plt.title("Question Accuracy")
plt.ylabel("Accuracy")
plt.show()

# ------------------------------
# 11. DIFFICULTY LEVEL
# ------------------------------
def difficulty(acc):
    if acc > 0.8:
        return "Easy"
    elif acc >= 0.5:
        return "Medium"
    else:
        return "Hard"

question_df["Difficulty"] = question_df["Accuracy"].apply(difficulty)

print("\n📌 Difficulty Level:\n")
print(question_df)

# ------------------------------
# 12. SAVE OUTPUT
# ------------------------------
df.to_excel("quiz_analysis.xlsx", index=False)

print("\n✅ Excel Report Generated: quiz_analysis.xlsx")