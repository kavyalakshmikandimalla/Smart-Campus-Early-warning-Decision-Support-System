import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.graph_objects as go
import plotly.express as px

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Smart Campus Early-Warning System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# FILES
# =========================================================

MODEL_FILE = "risk_model.pkl"
COLUMNS_FILE = "model_columns.pkl"
ENCODER_FILE = "risk_label_encoder.pkl"
DATASET_FILE = "smart_campus(1).csv"

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#eef7ff 0%,#f4fff9 100%);
}

.block-container {
    padding-top: 1.5rem;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg,#063b91,#087f5b);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 5px;
}

.metric-card {
    background: white;
    padding: 20px 10px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(0,0,0,0.08);
    border: 1px solid #e4edf6;
}

.metric-title {
    color: #667085;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #063b91;
    font-size: 27px;
    font-weight: 800;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    border: 1px solid #e4edf6;
    margin-bottom: 20px;
}

.low-card {
    background: #eafaf0;
    border-left: 8px solid #16a34a;
    padding: 25px;
    border-radius: 18px;
}

.medium-card {
    background: #fff8df;
    border-left: 8px solid #e0a000;
    padding: 25px;
    border-radius: 18px;
}

.high-card {
    background: #ffe9e9;
    border-left: 8px solid #dc2626;
    padding: 25px;
    border-radius: 18px;
}

div.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 12px;
    border: 1px solid #d7e5f2;
    background: #f8fbff;
    color: #063b91;
    font-weight: 600;
}

div.stButton > button:hover {
    background: #e8f3ff;
    border-color: #0b5ed7;
}

.footer {
    margin-top: 40px;
    padding: 25px;
    text-align: center;
    color: white;
    background: #08244f;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    model = None
    columns = None
    encoder = None

    if os.path.exists(MODEL_FILE):
        try:
            with open(MODEL_FILE, "rb") as f:
                model = pickle.load(f)
        except:
            model = None

    if os.path.exists(COLUMNS_FILE):
        try:
            with open(COLUMNS_FILE, "rb") as f:
                columns = pickle.load(f)
        except:
            columns = None

    if os.path.exists(ENCODER_FILE):
        try:
            with open(ENCODER_FILE, "rb") as f:
                encoder = pickle.load(f)
        except:
            encoder = None

    return model, columns, encoder


model, model_columns, label_encoder = load_model()

# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_dataset():

    if os.path.exists(DATASET_FILE):
        try:
            return pd.read_csv(DATASET_FILE)
        except:
            return None

    return None


dataset = load_dataset()

records = len(dataset) if dataset is not None else 0

# =========================================================
# SESSION STATE
# =========================================================

if "menu" not in st.session_state:
    st.session_state.menu = "Home"

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="text-align:center;padding:10px;">

<div style="font-size:45px;">🏫</div>

<h2 style="color:#063b91;margin:0;">
Smart Campus
</h2>

<p style="color:#667085;">
Early-Warning System
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# =========================================================
# RISK CATEGORIES
# =========================================================

st.sidebar.markdown(
    "<h3 style='color:#063b91;'>📊 Risk Categories</h3>",
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Select Risk Category",
    [
        "👨‍🎓 Student Risk",
        "🏫 Campus Risk",
        "🌦️ Environmental Risk"
    ]
)

# =========================================================
# QUICK INSIGHTS
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<h3 style='color:#063b91;'>📌 Quick Insights</h3>",
    unsafe_allow_html=True
)

if st.sidebar.button(
    "🎯 Prediction",
    use_container_width=True
):
    st.session_state.menu = "Prediction"

if st.sidebar.button(
    "🛡️ System",
    use_container_width=True
):
    st.session_state.menu = "System"

# =========================================================
# ANALYTICS
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<h3 style='color:#063b91;'>📈 Analytics</h3>",
    unsafe_allow_html=True
)

if st.sidebar.button(
    "📊 Performance Analysis",
    use_container_width=True
):
    st.session_state.menu = "Performance Analysis"

if st.sidebar.button(
    "⚠️ Risk Factor Analysis",
    use_container_width=True
):
    st.session_state.menu = "Risk Factor Analysis"

if st.sidebar.button(
    "🎯 Risk Score",
    use_container_width=True
):
    st.session_state.menu = "Risk Score"

if st.sidebar.button(
    "💡 Recommendations",
    use_container_width=True
):
    st.session_state.menu = "Recommendations"

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<h1>🏫 Smart Campus</h1>

<p>
<b>AI-Based Early-Warning Decision Support System</b>
</p>

<p>
📊 Monitor &nbsp; • &nbsp;
🎯 Predict &nbsp; • &nbsp;
⚠️ Prevent &nbsp; • &nbsp;
🛡️ Protect
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# TOP METRICS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">📂 Dataset Records</div>
        <div class="metric-value">{records}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">🤖 ML Model</div>
        <div class="metric-value">
        {"READY" if model else "OFF"}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">🎯 Prediction</div>
        <div class="metric-value">LIVE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">📊 Analytics</div>
        <div class="metric-value">ACTIVE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">🛡️ System</div>
        <div class="metric-value">ACTIVE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =========================================================
# VARIABLES
# =========================================================

risk_score = 0
risk = "LOW"
factors = []
recommendation = ""

performance_data = None

# =========================================================
# STUDENT RISK
# =========================================================

if page == "👨‍🎓 Student Risk":

    st.markdown("""
    <div class="card">

    <h2>👨‍🎓 Student Risk Prediction</h2>

    <p>
    Enter student academic information.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        attendance = st.slider(
            "👥 Attendance (%)",
            0,
            100,
            75
        )

        current_gpa = st.slider(
            "⭐ Current GPA",
            0.0,
            10.0,
            7.0,
            0.1
        )

        previous_gpa = st.slider(
            "📚 Previous GPA",
            0.0,
            10.0,
            7.0,
            0.1
        )

    with col2:

        assignment_rate = st.slider(
            "📝 Assignment Completion (%)",
            0,
            100,
            75
        )

        backlogs = st.number_input(
            "⚠️ Number of Backlogs",
            0,
            20,
            0
        )

    if attendance < 75:
        risk_score += 20
        factors.append("Attendance is below 75%")

    if current_gpa < 7:
        risk_score += 20
        factors.append("Current GPA is below 7")

    if previous_gpa < 7:
        risk_score += 10
        factors.append("Previous GPA is below 7")

    if assignment_rate < 75:
        risk_score += 20
        factors.append("Assignment completion is below 75%")

    if backlogs > 0:
        risk_score += 30
        factors.append(
            f"{int(backlogs)} backlog(s) detected"
        )

    risk_score = min(risk_score, 100)

    performance_data = pd.DataFrame({

        "Parameter": [
            "Attendance",
            "Current GPA",
            "Previous GPA",
            "Assignment Rate"
        ],

        "Current": [
            attendance,
            current_gpa * 10,
            previous_gpa * 10,
            assignment_rate
        ],

        "Normal": [
            75,
            70,
            70,
            75
        ]

    })

    if risk_score <= 20:
        risk = "LOW"

    elif risk_score <= 50:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    if risk == "HIGH":

        recommendation = (
            "Immediate academic intervention, faculty "
            "counselling and close monitoring are recommended."
        )

    elif risk == "MEDIUM":

        recommendation = (
            "Regular academic monitoring and improvement "
            "of weak areas are recommended."
        )

    else:

        recommendation = (
            "Student performance is within the normal range. "
            "Continue regular monitoring."
        )

# =========================================================
# CAMPUS RISK
# =========================================================

elif page == "🏫 Campus Risk":

    st.markdown("""
    <div class="card">

    <h2>🏫 Campus Risk Prediction</h2>

    <p>
    Enter campus performance information.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        campus_attendance = st.slider(
            "👥 Student Attendance (%)",
            0,
            100,
            80
        )

        infrastructure = st.slider(
            "🏢 Infrastructure Condition (%)",
            0,
            100,
            85
        )

        faculty = st.slider(
            "👨‍🏫 Faculty Availability (%)",
            0,
            100,
            90
        )

    with col2:

        safety = st.slider(
            "🏥 Health & Safety (%)",
            0,
            100,
            90
        )

        security = st.slider(
            "🔐 Campus Security (%)",
            0,
            100,
            90
        )

        academic = st.slider(
            "📚 Academic Performance (%)",
            0,
            100,
            80
        )

    campus_names = [
        "Attendance",
        "Infrastructure",
        "Faculty",
        "Health & Safety",
        "Security",
        "Academic"
    ]

    campus_values = [
        campus_attendance,
        infrastructure,
        faculty,
        safety,
        security,
        academic
    ]

    # Convert good performance into risk score
    risk_score = int(
        100 - np.mean(campus_values)
    )

    risk_score = max(
        0,
        min(risk_score, 100)
    )

    if campus_attendance < 75:
        factors.append(
            "Student attendance is below 75%"
        )

    if infrastructure < 70:
        factors.append(
            "Infrastructure condition needs attention"
        )

    if faculty < 70:
        factors.append(
            "Faculty availability is low"
        )

    if safety < 70:
        factors.append(
            "Health and safety score is low"
        )

    if security < 70:
        factors.append(
            "Campus security score is low"
        )

    if academic < 70:
        factors.append(
            "Academic performance is low"
        )

    performance_data = pd.DataFrame({

        "Parameter": campus_names,

        "Current": campus_values,

        "Normal": [
            75,
            75,
            75,
            75,
            75,
            75
        ]

    })

    if risk_score <= 20:
        risk = "LOW"

    elif risk_score <= 40:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    if risk == "HIGH":

        recommendation = (
            "Immediate institutional attention is required. "
            "Review infrastructure, safety, security and "
            "academic support systems."
        )

    elif risk == "MEDIUM":

        recommendation = (
            "Campus indicators should be monitored regularly "
            "and weak areas should be improved."
        )

    else:

        recommendation = (
            "Campus performance is within an acceptable range."
        )

# =========================================================
# ENVIRONMENTAL RISK
# =========================================================

else:

    st.markdown("""
    <div class="card">

    <h2>🌦️ Environmental Risk Prediction</h2>

    <p>
    Enter environmental condition information.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        temperature = st.slider(
            "🌡️ Temperature (°C)",
            0,
            50,
            28
        )

        humidity = st.slider(
            "💧 Humidity (%)",
            0,
            100,
            60
        )

        rainfall = st.slider(
            "🌧️ Rainfall (mm)",
            0,
            300,
            20
        )

    with col2:

        air_quality = st.slider(
            "🌬️ Air Quality Index",
            0,
            500,
            80
        )

        wind = st.slider(
            "🌪️ Wind Speed (km/h)",
            0,
            150,
            20
        )

        flood = st.slider(
            "🌊 Flood Risk (%)",
            0,
            100,
            10
        )

    if temperature > 40:
        risk_score += 25
        factors.append(
            "Temperature is above 40°C"
        )

    if humidity > 85:
        risk_score += 15
        factors.append(
            "Humidity is very high"
        )

    if rainfall > 100:
        risk_score += 20
        factors.append(
            "Heavy rainfall detected"
        )

    if air_quality > 150:
        risk_score += 20
        factors.append(
            "Air Quality Index is high"
        )

    if wind > 80:
        risk_score += 10
        factors.append(
            "High wind speed detected"
        )

    if flood > 50:
        risk_score += 20
        factors.append(
            "High flood risk detected"
        )

    risk_score = min(
        risk_score,
        100
    )

    performance_data = pd.DataFrame({

        "Parameter": [
            "Temperature",
            "Humidity",
            "Rainfall",
            "Air Quality",
            "Wind Speed",
            "Flood Risk"
        ],

        "Current": [
            temperature,
            humidity,
            rainfall,
            air_quality,
            wind,
            flood
        ]

    })

    if risk_score <= 20:
        risk = "LOW"

    elif risk_score <= 40:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    if risk == "HIGH":

        recommendation = (
            "Immediate environmental safety precautions "
            "and continuous monitoring are recommended."
        )

    elif risk == "MEDIUM":

        recommendation = (
            "Environmental conditions should be monitored "
            "regularly and preventive measures should be taken."
        )

    else:

        recommendation = (
            "Environmental conditions are currently "
            "within an acceptable range."
        )

# =========================================================
# SIDEBAR - PREDICTION
# =========================================================

if st.session_state.menu == "Prediction":

    st.markdown(
        f"## 🎯 {page} - Prediction"
    )

    if risk == "HIGH":

        st.error(
            f"🔴 HIGH RISK — Risk Score: {risk_score}%"
        )

    elif risk == "MEDIUM":

        st.warning(
            f"🟡 MEDIUM RISK — Risk Score: {risk_score}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — Risk Score: {risk_score}%"
        )

    st.info(
        f"{page} prediction system is LIVE and ACTIVE."
    )

# =========================================================
# SIDEBAR - SYSTEM
# =========================================================

elif st.session_state.menu == "System":

    st.markdown(
        f"## 🛡️ {page} - System"
    )

    st.success(
        f"🟢 {page} System is ACTIVE."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Prediction",
            "LIVE"
        )

    with c2:
        st.metric(
            "Analytics",
            "ACTIVE"
        )

    with c3:
        st.metric(
            "System",
            "ACTIVE"
        )

# =========================================================
# PERFORMANCE ANALYSIS
# =========================================================

elif st.session_state.menu == "Performance Analysis":

    st.markdown(
        f"## 📊 {page} - Performance Analysis"
    )

    if page == "🌦️ Environmental Risk":

        chart = px.bar(
            performance_data,
            x="Parameter",
            y="Current",
            text="Current",
            title="🌦️ Environmental Performance"
        )

    else:

        long_data = performance_data.melt(
            id_vars="Parameter",
            var_name="Type",
            value_name="Value"
        )

        chart = px.bar(
            long_data,
            x="Parameter",
            y="Value",
            color="Type",
            barmode="group",
            text="Value",
            title=f"{page} Performance Analysis"
        )

    chart.update_layout(
        height=450
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

# =========================================================
# RISK FACTOR ANALYSIS
# =========================================================

elif st.session_state.menu == "Risk Factor Analysis":

    st.markdown(
        f"## ⚠️ {page} - Risk Factor Analysis"
    )

    # NO CHART

    if factors:

        st.warning(
            "The following risk factors were detected:"
        )

        for factor in factors:

            st.markdown(
                f"""
                <div style="
                    background:#fff8df;
                    padding:15px;
                    border-radius:12px;
                    margin:8px 0;
                    border-left:5px solid #e0a000;
                ">

                ⚠️ <b>{factor}</b>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "✅ No significant risk factors detected."
        )

    st.markdown(
        "### 🎯 Overall Risk"
    )

    if risk == "HIGH":

        st.error(
            f"🔴 HIGH RISK — Risk Score: {risk_score}%"
        )

    elif risk == "MEDIUM":

        st.warning(
            f"🟡 MEDIUM RISK — Risk Score: {risk_score}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — Risk Score: {risk_score}%"
        )

# =========================================================
# RISK SCORE
# =========================================================

elif st.session_state.menu == "Risk Score":

    st.markdown(
        f"## 🎯 {page} - Risk Score"
    )

    if risk == "HIGH":

        st.markdown(
            f"""
            <div class="high-card">

            <h1>🔴 HIGH RISK</h1>

            <h2>
            Risk Score: {risk_score}%
            </h2>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif risk == "MEDIUM":

        st.markdown(
            f"""
            <div class="medium-card">

            <h1>🟡 MEDIUM RISK</h1>

            <h2>
            Risk Score: {risk_score}%
            </h2>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="low-card">

            <h1>🟢 LOW RISK</h1>

            <h2>
            Risk Score: {risk_score}%
            </h2>

            </div>
            """,
            unsafe_allow_html=True
        )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={
                "text": f"{page} Risk Score"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#d9f7df"
                    },
                    {
                        "range": [40, 70],
                        "color": "#fff0b8"
                    },
                    {
                        "range": [70, 100],
                        "color": "#ffd6d6"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=400
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

# =========================================================
# RECOMMENDATIONS
# =========================================================

elif st.session_state.menu == "Recommendations":

    st.markdown(
        f"## 💡 {page} - Recommendations"
    )

    if risk == "HIGH":

        st.error(
            recommendation
        )

    elif risk == "MEDIUM":

        st.warning(
            recommendation
        )

    else:

        st.success(
            recommendation
        )

    st.markdown(
        "### 📋 Current Status"
    )

    summary = pd.DataFrame({

        "Parameter": [
            "Risk Category",
            "Risk Score",
            "Risk Level"
        ],

        "Value": [
            page,
            f"{risk_score}%",
            risk
        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# HOME
# =========================================================

else:

    st.markdown("""
    <div class="card">

    <h2>
    👈 Select an option from the sidebar
    </h2>

    <p>
    Choose Prediction, System,
    Performance Analysis, Risk Factor Analysis,
    Risk Score or Recommendations.
    </p>

    <p>
    The selected option will automatically
    show results for the currently selected
    Student, Campus or Environmental Risk.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

<h2>
🏫 Smart Campus Early-Warning System
</h2>

<p>
🤖 Artificial Intelligence
&nbsp; | &nbsp;
📊 Data Analytics
&nbsp; | &nbsp;
🎯 Risk Prediction
</p>

<p>
<b>
Monitor • Predict • Prevent • Protect
</b>
</p>

</div>
""", unsafe_allow_html=True)