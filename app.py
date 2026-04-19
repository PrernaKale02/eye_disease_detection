import streamlit as st
import cv2
import os

from load_models import load_all_models
from predict import predict_all
from ensemble import ensemble_decision
from explain import generate_explanations
from feature_extraction import generate_text_explanation
from clinical_explainer import build_clinical_report
from keywords_config import DISEASE_CONFIG


# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="Retinal Disease Detection",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #050d1a;
    color: #e8edf5;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero {
    background: linear-gradient(135deg, #060f20 0%, #0a1a35 50%, #061428 100%);
    border-bottom: 1px solid #1a2d50;
    padding: 48px 64px 40px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -80px;
    right: -80px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,180,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00b4ff;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 42px;
    font-weight: 400;
    color: #f0f5ff;
    line-height: 1.1;
    margin: 0 0 10px;
}

.hero-title span { color: #00b4ff; }

.hero-sub {
    font-size: 15px;
    color: #6b85a8;
    font-weight: 300;
    max-width: 520px;
}

.main-content {
    padding: 40px 64px;
    max-width: 1400px;
    margin: 0 auto;
}

.card {
    background: #0a1628;
    border: 1px solid #1a2d50;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
}

.card-accent { border-left: 3px solid #00b4ff; }

.card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #3a5580;
    margin-bottom: 16px;
}

.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #c8d8f0;
    margin-bottom: 6px;
    font-weight: 400;
}

[data-testid="stFileUploader"] {
    background: #060f1e !important;
    border: 2px dashed #1a2d50 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    transition: border-color 0.2s;
}

[data-testid="stFileUploader"]:hover {
    border-color: #00b4ff !important;
}

[data-testid="stFileUploader"] label {
    color: #6b85a8 !important;
}

.stSpinner > div {
    border-top-color: #00b4ff !important;
}

[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #1a2d50;
}

[data-testid="column"] { padding: 0 12px; }

.img-caption {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3a5580;
    text-align: center;
    margin-top: 8px;
}

.h-divider {
    border: none;
    border-top: 1px solid #0f1e35;
    margin: 32px 0;
}

.report-box {
    background: #060f1e;
    border: 1px solid #1a2d50;
    border-radius: 8px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px;
    line-height: 1.9;
    color: #8aa8d0;
    white-space: pre-wrap;
}

.analysis-box {
    background: #060f1e;
    border: 1px solid #1a2d50;
    border-radius: 8px;
    padding: 20px 24px;
    color: #c8d8f0;
    min-height: 100%;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}

.analysis-box p {
    margin: 0 0 12px;
    color: #8aa0c0;
}

.analysis-box strong {
    color: #f0f5ff;
}

.disease-name {
    font-family: 'DM Serif Display', serif;
    font-size: 26px;
    line-height: 1.15;
    color: #f5f8ff;
    margin: 0 0 14px;
    text-shadow: 0 0 20px rgba(0, 180, 255, 0.08);
}

.disease-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5f7ea8;
    margin: 0 0 12px;
}

.risk-chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid #1a2d50;
    margin-bottom: 14px;
}

.risk-chip.high,
.info-box.high {
    color: #ffd6d6;
    border-color: #ff5a5f;
    background: linear-gradient(135deg, rgba(58,10,14,0.98), rgba(24,10,16,0.98));
    box-shadow: 0 0 0 1px rgba(255,90,95,0.08), 0 10px 30px rgba(255,90,95,0.12);
}

.risk-chip.moderate,
.risk-chip.medium,
.info-box.moderate,
.info-box.medium {
    color: #ffe2bf;
    border-color: #ffb347;
    background: linear-gradient(135deg, rgba(51,26,8,0.98), rgba(24,14,10,0.98));
    box-shadow: 0 0 0 1px rgba(255,179,71,0.08), 0 10px 30px rgba(255,179,71,0.1);
}

.risk-chip.low,
.info-box.low {
    color: #d4ffeb;
    border-color: #00e0a0;
    background: linear-gradient(135deg, rgba(8,26,20,0.98), rgba(10,22,40,0.98));
    box-shadow: 0 0 0 1px rgba(0,224,160,0.08), 0 10px 30px rgba(0,224,160,0.08);
}

.risk-chip.unknown {
    color: #dbe8ff;
    border-color: #4f6b92;
    background: linear-gradient(135deg, rgba(12,22,40,0.98), rgba(10,22,40,0.98));
}

.feature-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #8aa8d0;
    margin: 0 0 6px;
}

.info-box {
    border: 1px solid #1a2d50;
    border-left: 3px solid currentColor;
    border-radius: 8px;
    padding: 16px 18px;
    position: relative;
}

.metric-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(26, 45, 80, 0.75);
}

.metric-line:last-of-type {
    margin-bottom: 16px;
}

.metric-value {
    color: #f0f5ff;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Clinical AI · Ophthalmology</div>
    <div class="hero-title">Retinal<span> Disease Detection</span></div>
    <div class="hero-sub">Upload a fundus image to analyze retinal diseases using AI.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ------------------------------------------------
# Load models once
# ------------------------------------------------
@st.cache_resource
def load_ai_models():
    return load_all_models()

models = load_ai_models()


# ------------------------------------------------
# Image uploader
# ------------------------------------------------
st.markdown("""
<div class="card card-accent">
    <div class="card-label">Step 01 — Input</div>
    <div class="card-title">Upload Fundus Image</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Fundus Image",
    type=["jpg", "png", "jpeg"]
)


if uploaded_file is not None:

    os.makedirs("temp", exist_ok=True)

    image_path = os.path.join("temp", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Preview</div>
            <div class="card-title">Uploaded Image</div>
        </div>
        """, unsafe_allow_html=True)
        st.image(image_path, use_container_width=True)
        st.markdown(f'<div class="img-caption">{uploaded_file.name}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-label">Analysis</div>
            <div class="card-title">Running AI Analysis...</div>
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Analyzing retinal image..."):

            model_results = predict_all(image_path)
            final_result = ensemble_decision(model_results)

    # ------------------------------------------------
    # Diagnosis report
    # ------------------------------------------------
    st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-label">Step 02 — Diagnosis Report</div>
    <div class="card-title" style="margin-bottom:16px;">Diagnosis Report</div>
    """, unsafe_allow_html=True)

    report = generate_text_explanation(final_result, model_results)

    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)

    # ------------------------------------------------
    # Grad-CAM + Clinical analysis
    # ------------------------------------------------
    detected_diseases = [d[0] for d in final_result["detected_conditions"]]

    explanations = generate_explanations(
        image_path,
        models,
        detected_diseases
    )

    st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-label">Step 03 — Explainable AI Analysis</div>
    <div class="card-title" style="margin-bottom:20px;">Explainable AI Analysis</div>
    """, unsafe_allow_html=True)

    ordered = final_result["detected_conditions"]

    for disease, _ in ordered:
        data = explanations[disease]

        img = data["image"]
        keywords = data["keywords"]

        prediction = model_results[DISEASE_CONFIG[disease]["model_key"]]["prediction"]
        confidence = model_results[DISEASE_CONFIG[disease]["model_key"]]["confidence"]

        report = build_clinical_report(
            disease,
            prediction,
            confidence,
            keywords
        )
        risk_text = str(report["risk"]).strip()
        risk_key = risk_text.lower()
        if "high" in risk_key or "severe" in risk_key:
            risk_class = "high"
        elif "moderate" in risk_key or "medium" in risk_key:
            risk_class = "moderate"
        elif "low" in risk_key or "mild" in risk_key:
            risk_class = "low"
        else:
            risk_class = "unknown"

        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">Grad-CAM</div>
                <div class="card-title">{disease} Grad-CAM</div>
            </div>
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)

        with col2:
            st.markdown("""
            <div class="card">
                <div class="card-label">Clinical Review</div>
                <div class="card-title">Clinical Analysis</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
            st.markdown('<div class="disease-sub">Detected Condition</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="disease-name">{disease}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="risk-chip {risk_class}">{report["risk"]} Risk</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-line"><strong>Stage:</strong><span class="metric-value">{report["stage"]}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-line"><strong>Risk Level:</strong><span class="metric-value">{report["risk"]}</span></div>', unsafe_allow_html=True)
            st.markdown("<p><strong>Explanation:</strong></p>", unsafe_allow_html=True)
            st.markdown(f"<p>{report['explanation']}</p>", unsafe_allow_html=True)
            st.markdown("<p><strong>Detected Features:</strong></p>", unsafe_allow_html=True)
            if keywords:
                for k in keywords:
                    st.markdown(f'<div class="feature-item">• {k}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="feature-item">• retinal activation detected</div>', unsafe_allow_html=True)

            st.markdown("<p><strong>Clinical Recommendation:</strong></p>", unsafe_allow_html=True)
            st.markdown(f'<div class="info-box {risk_class}">{report["advice"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
