import streamlit as st
import pandas as pd
from db_connection import get_connection
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("Placement Eligibility Dashboard")

menu = st.sidebar.radio("Navigation", ["Eligibility Checker", "Insights Dashboard", "SQL Search"])

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# ELIGIBILITY CHECKER
if menu == "Eligibility Checker":

    st.subheader("Check Eligible Students")

    # ---------------- SQL Preview Section ----------------
    st.markdown("### View All Students (SQL Demo)")
    st.code("SELECT * FROM students ORDER BY student_id ASC;", language="sql")

    if st.button("Submit"):
        df = pd.read_sql("""
            SELECT * FROM students
            ORDER BY CAST(student_id AS UNSIGNED) ASC
        """, con=conn)

        st.dataframe(df, use_container_width=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        min_problems = st.slider("Minimum Problems Solved", 0, 500, 100)

    with col2:
        min_mock = st.slider("Minimum Mock Interview Score", 0, 100, 70)

    with col3:
        min_comm = st.slider("Minimum Communication Score", 0, 100, 75)

    placement_status = st.selectbox(
        "Placement Status",
        ["All", "Placed", "Ready", "Not Ready", "Seeking"]
    )

    if st.button("Apply Filters"):

        query = """
        SELECT s.student_id, s.name, s.course_batch, s.city,
               pr.problems_solved,
               ss.communication,
               pl.mock_interview_score,
               pl.placement_status
        FROM students s
        JOIN programming pr ON s.student_id = pr.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pr.problems_solved >= %s
        AND pl.mock_interview_score >= %s
        AND ss.communication >= %s
        """

        params = [min_problems, min_mock, min_comm]

        if placement_status != "All":
            query += " AND pl.placement_status = %s"
            params.append(placement_status)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if rows:
            df = pd.DataFrame(rows)
            st.success(f"Found {len(df)} students")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "eligible_students.csv")

        else:
            st.warning("No students found matching criteria")

# INSIGHTS DASHBOARD – 10 QUERIES
elif menu == "Insights Dashboard":

    st.subheader("Placement Insights")

    # ---------------- KPI SECTION ----------------
    col1, col2, col3 = st.columns(3)

    cursor.execute("SELECT COUNT(*) as total FROM students")
    total_students = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as placed FROM placements WHERE placement_status='Placed'")
    placed_students = cursor.fetchone()['placed']

    cursor.execute("SELECT AVG(placement_package) as avg_pkg FROM placements WHERE placement_status='Placed'")
    avg_package = cursor.fetchone()['avg_pkg']

    col1.metric("Total Students", total_students)
    col2.metric("Placed Students", placed_students)
    col3.metric("Average Package", f"${round(avg_package,2) if avg_package else 0}")

    st.markdown("---")

    # 1 Top 5 Students by Mock Score
    st.markdown("### 1. Top 5 Students by Mock Score")
    cursor.execute("""
        SELECT s.name, pl.mock_interview_score
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        ORDER BY pl.mock_interview_score DESC
        LIMIT 5
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 2 Batch-wise Average Problems Solved
    st.markdown("### 2. Batch-wise Average Problems Solved")
    cursor.execute("""
        SELECT s.course_batch, AVG(pr.problems_solved) as avg_problems
        FROM students s
        JOIN programming pr ON s.student_id = pr.student_id
        GROUP BY s.course_batch
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 3 Programming Language Popularity
    st.markdown("### 3. Programming Language Distribution")
    cursor.execute("""
        SELECT language, COUNT(*) as count
        FROM programming
        GROUP BY language
        ORDER BY count DESC
    """)
    st.bar_chart(pd.DataFrame(cursor.fetchall()).set_index("language"))

    # 4 Language-wise Placement Rate
    st.markdown("### 4. Placement Rate by Language")
    cursor.execute("""
        SELECT pr.language,
        COUNT(CASE WHEN pl.placement_status='Placed' THEN 1 END)*100.0/COUNT(*) as placement_percentage
        FROM programming pr
        JOIN placements pl ON pr.student_id = pl.student_id
        GROUP BY pr.language
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 5 Gender-wise Placement
    st.markdown("### 5. Gender-wise Placement Percentage")
    cursor.execute("""
        SELECT s.gender,
        COUNT(CASE WHEN p.placement_status='Placed' THEN 1 END)*100.0/COUNT(*) as percentage
        FROM students s
        JOIN placements p ON s.student_id = p.student_id
        GROUP BY s.gender
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 6 Internship vs Placement
    st.markdown("### 6. Internship Count vs Placement")
    cursor.execute("""
        SELECT internships_completed,
        COUNT(CASE WHEN placement_status='Placed' THEN 1 END) as placed,
        COUNT(*) as total
        FROM placements
        GROUP BY internships_completed
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 7 Average Package by Language
    st.markdown("### 7. Average Package by Programming Language")
    cursor.execute("""
        SELECT pr.language, AVG(pl.placement_package) as avg_package
        FROM programming pr
        JOIN placements pl ON pr.student_id = pl.student_id
        WHERE pl.placement_status='Placed'
        GROUP BY pr.language
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 8 Top 5 Cities by Placement
    st.markdown("### 8. Top Cities by Placement")
    cursor.execute("""
        SELECT s.city, COUNT(*) as placements
        FROM placements p
        JOIN students s ON p.student_id = s.student_id
        WHERE p.placement_status='Placed'
        GROUP BY s.city
        ORDER BY placements DESC
        LIMIT 5
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 9 Soft Skills Comparison (Placed vs Not)
    st.markdown("### 9. Soft Skills Comparison")
    cursor.execute("""
        SELECT p.placement_status,
        AVG(s.communication) as avg_comm,
        AVG(s.teamwork) as avg_teamwork,
        AVG(s.presentation) as avg_presentation
        FROM soft_skills s
        JOIN placements p ON s.student_id = p.student_id
        GROUP BY p.placement_status
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

    # 10 High Project Score but Not Placed
    st.markdown("### 10. High Project Score but Not Placed")
    cursor.execute("""
        SELECT s.name, pr.latest_project_score
        FROM programming pr
        JOIN students s ON pr.student_id = s.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pr.latest_project_score >= 90
        AND pl.placement_status != 'Placed'
    """)
    st.table(pd.DataFrame(cursor.fetchall()))

# SQL SEARCH (QUERY RUNNER)
elif menu == "SQL Search":

    st.subheader("Secure SQL / Question Search")

    st.markdown("""
    Allowed: SELECT queries  
    Not Allowed: DROP, DELETE, UPDATE, INSERT, ALTER
    """)

    user_input = st.text_area(
        "Write your SQL query or question:",
        height=150,
        placeholder="Example: SELECT * FROM students;"
    )

    if st.button("Run Query", key="secure_sql_runner"):

        if user_input.strip() == "":
            st.warning("Please enter a query.")
        else:
            try:
                input_clean = user_input.strip().lower()

                # Block Dangerous Keywords
                dangerous_keywords = [
                    "drop", "delete", "update",
                    "insert", "alter", "truncate",
                    "create", "replace"
                ]

                if any(word in input_clean for word in dangerous_keywords):
                    st.error("Dangerous SQL command detected. Only SELECT queries are allowed.")
                    st.stop()
                    
                # Allow Only SELECT
                if not input_clean.startswith("select"):
                    st.error("Only SELECT queries are allowed.")
                    st.stop()

                # Execute Safe Query
                df = pd.read_sql(user_input, con=conn)

                st.success("Query executed safely!")
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"Error executing query: {e}")

conn.close()
