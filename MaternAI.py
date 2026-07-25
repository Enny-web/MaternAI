# Import the necessary libraries
import streamlit as st
import pandas as pd
import joblib
from openai import OpenAI
import base64

# Function to Add Background Image

def add_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# Openrouter API


client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Configure Page
st.set_page_config(
    page_title="MaternAI",
    page_icon="🤰",
    layout="centered"
)

# Add the background image
add_bg("image.jpg")

# Custom CSS Styling

st.markdown(
    """
<style>

/* =========================
   Main Title
========================= */

h1 {
    color: white !important;
    text-align: center;
}

/* =========================
   Subheaders
========================= */

h2, h3, h4, h5, h6 {
    color: white !important;
}

/* =========================
   Main App Text
========================= */

.stApp,
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span,
.stApp span,
.stApp div,
p,
li {
    color: white !important;
}

/* =========================
   Widget Labels
========================= */

label,
div[data-testid="stWidgetLabel"] p {
    color: white !important;
}

/* =========================
   Input Text
========================= */

input {
    color: white !important;
}

/* =========================
   Sidebar
========================= */

section[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.95);
}

section[data-testid="stSidebar"] * {
    color: black !important;
}

/* =========================
   Buttons
========================= */

div.stButton > button {
    background-color: #1565C0;
    color: white !important;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #0B5394;
    color: white !important;
}

div.stButton > button p,
div.stButton > button span {
    color: white !important;
}

/* =========================
   Input Boxes
========================= */

div[data-baseweb="input"] > div {
    border-radius: 10px;
}

/* =========================
   Metric Cards
========================= */

div[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.95);
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #E3F2FD;
}

/* Make metric text black since the card is white */
div[data-testid="metric-container"] * {
    color: black !important;
}

</style>
""",
    unsafe_allow_html=True
)

# App Title and Introduction

st.title("MaternAI")

st.markdown(
    """
### AI-Powered Maternal Health Risk Prediction System
"""
)

st.info(
    """
Enter the patient's clinical measurements below to predict maternal health risk.

**Disclaimer:** This application is intended for educational purposes only and does not replace professional medical advice.
"""
)

st.divider()

# Load Model and Encoder

model = joblib.load("maternal_health_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Sidebar
with st.sidebar:

    st.title("MaternAI")

    st.markdown("---")

    st.markdown("## About")

    st.write(
        """
MaternAI predicts maternal health risk using an optimized XGBoost machine learning model trained on maternal clinical data.

The application also provides an AI-generated explanation to help users better understand the prediction.
"""
    )

    st.markdown("---")

    st.markdown("### Clinical Features")

    st.write(
        """
- Age
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Blood Sugar
- Body Temperature
- Heart Rate
"""
    )

    st.markdown("---")

    st.info(
        "⚠️ This application is intended for educational purposes only and should not replace professional medical advice."
    )

    st.markdown("---")

# Patient Information

with st.container():

    st.subheader("Patient Clinical Information")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=70,
            value=25
        )

        sbp = st.number_input(
            "Systolic Blood Pressure (mmHg)",
            min_value=70,
            max_value=200,
            value=120
        )

        dbp = st.number_input(
            "Diastolic Blood Pressure (mmHg)",
            min_value=40,
            max_value=130,
            value=80
        )

    with col2:

        bs = st.number_input(
            "Blood Sugar (mmol/L)",
            min_value=2.0,
            max_value=20.0,
            value=6.0,
            step=0.1
        )

        temp = st.number_input(
            "Body Temperature (°F)",
            min_value=95.0,
            max_value=105.0,
            value=98.6,
            step=0.1
        )

        hr = st.number_input(
            "Heart Rate (bpm)",
            min_value=40,
            max_value=180,
            value=80
        )

# Prediction Button

st.write("")
st.write("")

if st.button("Predict Risk", use_container_width=True):

    # Create DataFrame
    input_data = pd.DataFrame({
        "Age": [age],
        "SystolicBP": [sbp],
        "DiastolicBP": [dbp],
        "BS": [bs],
        "BodyTemp": [temp],
        "HeartRate": [hr]
    })

    # Predict
    with st.spinner("Analyzing your data..."):
        prediction = model.predict(input_data)

    # Decode prediction
    risk_level = encoder.inverse_transform(prediction)[0]

    # Gemini Prompt
    sprompt = f"""
You are MaternAI, an AI maternal healthcare assistant.

A machine learning model predicted that this patient has a pregnancy risk level of:

{risk_level}

Patient Details

Age: {age} years
Systolic Blood Pressure: {sbp} mmHg
Diastolic Blood Pressure: {dbp} mmHg
Blood Sugar: {bs} mmol/L
Body Temperature: {temp} °F
Heart Rate: {hr} bpm

Generate a professional maternal health report using the following headings:

## 🩺 Risk Assessment
Briefly explain the predicted risk level.

## 📊 Clinical Findings
Identify which measurements are outside normal ranges and explain why they may have contributed to the prediction.

## 💡 What This Means
Explain the result in simple language suitable for someone without a medical background.

## 🌱 Healthy Lifestyle Recommendations
Provide practical advice on diet, hydration, rest, exercise, antenatal care, and medication adherence where appropriate.

## ⚠️ Disclaimer
State clearly that this AI provides educational information only and does not replace a qualified healthcare professional.

Do not diagnose diseases.
Do not prescribe medications.
Keep the tone warm, reassuring, and professional.
"""

    # Generate AI explanation

    try:
        with st.spinner("Generating AI explanation..."):

            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": sprompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )

            ai_response = response.choices[0].message.content

    except Exception as e:

        ai_response = f"""
###  AI Assistant Temporarily Unavailable

The maternal health risk prediction was successfully generated using the machine learning model.

**Predicted Risk Level:** {risk_level.title()}

The AI explanation service is currently unavailable.

**Error:**
{e}

Please consult a qualified healthcare professional for appropriate medical advice.
"""

    # Patient Summary

    st.divider()

    st.subheader("Patient Summary")

    st.dataframe(
        input_data,
        use_container_width=True,
        hide_index=True
    )

    # Prediction Result

    st.subheader("Prediction Result")

    st.metric(
        label="Predicted Risk",
        value=risk_level.title()
    )

    if risk_level == "low risk":
        st.success("🟢 Low Risk Pregnancy")

    elif risk_level == "mid risk":
        st.warning("🟡 Moderate Risk Pregnancy")

    else:
        st.error("🔴 High Risk Pregnancy")

    # ==========================
    # AI Health Assistant
    # ==========================

    st.divider()

    st.subheader("AI Health Assistant")

    st.write(ai_response)