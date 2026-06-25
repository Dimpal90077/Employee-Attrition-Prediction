import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.metric-card {
    padding: 15px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

h1,h2,h3 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("👨‍💼 HR Analytics")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard",
     "📊 Attrition Analysis",
     "🤖 Prediction",
     "💡 HR Recommendations"]
)

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------
if page == "🏠 Dashboard":

    st.title("👨‍💼 Employee Attrition Analytics Dashboard")
    st.markdown("### Predict • Analyze • Retain Talent")

    total_emp = len(df)
    attrition = len(df[df["Attrition"]=="Yes"])
    rate = round(attrition/total_emp*100,2)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("👥 Employees", total_emp)
    c2.metric("🚪 Left Company", attrition)
    c3.metric("📈 Attrition Rate", f"{rate}%")
    c4.metric("😊 Avg Age", round(df["Age"].mean(),1))

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        attrition_count = df["Attrition"].value_counts().reset_index()
        fig = px.pie(
            attrition_count,
            values="count",
            names="Attrition",
            title="Employee Attrition"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dep = px.bar(
            df.groupby("Department").size().reset_index(name="Employees"),
            x="Department",
            y="Employees",
            title="Employees by Department"
        )
        st.plotly_chart(dep, use_container_width=True)

# --------------------------------------------------
# ANALYSIS PAGE
# --------------------------------------------------
elif page == "📊 Attrition Analysis":

    st.title("📊 Attrition Insights")

    col1,col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df,
            x="Age",
            color="Attrition",
            title="Age Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        overtime = px.histogram(
            df,
            x="OverTime",
            color="Attrition",
            title="Overtime vs Attrition"
        )
        st.plotly_chart(overtime, use_container_width=True)

    st.info(
        "📌 Employees working overtime show significantly higher attrition."
    )

    st.warning(
        "⚠ Lower job satisfaction and lower income are common among employees who leave."
    )

# --------------------------------------------------
# PREDICTION PAGE
# --------------------------------------------------
elif page == "🤖 Prediction":

    st.title("🤖 Employee Attrition Prediction")

    age = st.slider("Age",18,60,30)
    income = st.number_input("Monthly Income",1000,50000,10000)

    overtime = st.selectbox(
        "OverTime",
        ["No","Yes"]
    )

    satisfaction = st.slider(
        "Job Satisfaction",
        1,4,2
    )

    years = st.slider(
        "Years At Company",
        0,40,5
    )

    if st.button("🔮 Predict Attrition"):

        # Example logic
        risk = 20

        if overtime=="Yes":
            risk += 30

        if satisfaction <=2:
            risk += 25

        if income < 5000:
            risk += 15

        if years < 2:
            risk += 10

        risk = min(risk,100)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            title={'text': "Attrition Risk Score"},
            gauge={
                'axis': {'range': [0,100]}
            }
        ))

        st.plotly_chart(fig,use_container_width=True)

        if risk > 60:
            st.error(
                f"🔴 High Attrition Risk ({risk}%)"
            )
        else:
            st.success(
                f"🟢 Low Attrition Risk ({risk}%)"
            )

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------
elif page == "💡 HR Recommendations":

    st.title("💡 HR Retention Recommendations")

    st.success("""
    ✅ Conduct stay interviews with employees
    working overtime.
    """)

    st.success("""
    ✅ Improve career growth opportunities for
    employees with low tenure.
    """)

    st.success("""
    ✅ Monitor employee satisfaction quarterly.
    """)

    st.success("""
    ✅ Review compensation for employees in
    high-risk roles.
    """)

    st.info("""
    📌 Salary alone does not explain attrition.
    Overtime, satisfaction, and career growth
    often have a stronger impact.
    """)