import streamlit as st
import cv2
import os

from load_models import load_all_models
from predict import predict_all
from ensemble import ensemble_decision
from explain import generate_explanations
from feature_extraction import generate_text_explanation

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetinaScan AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #050d1a;
    color: #e8edf5;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero banner ── */
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
    top: -80px; right: -80px;
    width: 400px; height: 400px;
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

/* ── Main content area ── */
.main-content {
    padding: 40px 64px;
    max-width: 1400px;
    margin: 0 auto;
}

/* ── Cards ── */
.card {
    background: #0a1628;
    border: 1px solid #1a2d50;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
}
.card-accent {
    border-left: 3px solid #00b4ff;
}
.card-success {
    border-left: 3px solid #00e0a0;
    background: linear-gradient(135deg, #081a14, #0a1628);
}
.card-warning {
    border-left: 3px solid #ffb347;
    background: linear-gradient(135deg, #1a1408, #0a1628);
}
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

/* ── Upload zone ── */
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

/* ── Progress / spinner ── */
.stSpinner > div {
    border-top-color: #00b4ff !important;
}

/* ── Status steps ── */
.step-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid #0f1e35;
}
.step-row:last-child { border-bottom: none; }
.step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00b4ff;
    box-shadow: 0 0 8px rgba(0,180,255,0.6);
    flex-shrink: 0;
    animation: pulse 1.4s infinite;
}
.step-dot.done { background: #00e0a0; box-shadow: 0 0 8px rgba(0,224,160,0.5); animation: none; }
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}
.step-label { font-size: 13px; color: #8aa0c0; font-weight: 400; }
.step-label.done { color: #00e0a0; }

/* ── Condition tags ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 4px; }
.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 5px 14px;
    border-radius: 20px;
    border: 1px solid;
    font-weight: 500;
    letter-spacing: 0.5px;
}
.tag-high   { color: #ff6b6b; border-color: #ff6b6b; background: rgba(255,107,107,0.08); }
.tag-medium { color: #ffb347; border-color: #ffb347; background: rgba(255,179,71,0.08); }
.tag-low    { color: #00e0a0; border-color: #00e0a0; background: rgba(0,224,160,0.08); }

/* ── Report text ── */
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
    max-height: 320px;
    overflow-y: auto;
}

/* ── XAI grid ── */
.xai-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 20px;
}
.xai-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #3a5580;
    letter-spacing: 1px;
}

/* ── Feature keyword pills ── */
.kw-pill {
    display: inline-block;
    background: #0f1e35;
    border: 1px solid #1a3055;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    color: #7090b8;
    margin: 3px 4px 3px 0;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Divider ── */
.h-divider {
    border: none;
    border-top: 1px solid #0f1e35;
    margin: 32px 0;
}

/* ── Image caption ── */
.img-caption {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3a5580;
    text-align: center;
    margin-top: 8px;
}

/* ── Streamlit image border ── */
[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #1a2d50;
}

/* ── Column gap ── */
[data-testid="column"] { padding: 0 12px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Clinical AI · Ophthalmology</div>
    <div class="hero-title">Retina<span>Scan</span> AI</div>
    <div class="hero-sub">Deep-learning ensemble analysis for automated retinal disease detection from fundus photography.</div>
</div>
""", unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.6], gap="large")

with left_col:
    # Upload card
    st.markdown("""
    <div class="card card-accent">
        <div class="card-label">Step 01 — Input</div>
        <div class="card-title">Upload Fundus Image</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drag & drop or browse — JPG, PNG, JPEG",
        type=["jpg", "png", "jpeg"],
        label_visibility="visible",
    )

    if uploaded_file is not None:
        image_path = os.path.join("test_images", uploaded_file.name)
        os.makedirs("test_images", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(image_path, use_container_width=True)
        st.markdown(f'<div class="img-caption">📁 {uploaded_file.name}</div>', unsafe_allow_html=True)

with right_col:
    if uploaded_file is not None:
        # Analysis pipeline card
        st.markdown("""
        <div class="card">
            <div class="card-label">Step 02 — Analysis Pipeline</div>
            <div class="card-title">Running Ensemble Inference</div>
        </div>
        """, unsafe_allow_html=True)

        # Step tracker
        steps = [
            ("Loading model ensemble", "done"),
            ("Running predictions", "done"),
            ("Ensemble voting", "done"),
            ("Generating report", "done"),
        ]
        steps_html = ""
        for label, state in steps:
            dot_cls = "step-dot done" if state == "done" else "step-dot"
            lbl_cls = "step-label done" if state == "done" else "step-label"
            steps_html += f"""
            <div class="step-row">
                <div class="{dot_cls}"></div>
                <span class="{lbl_cls}">{label}</span>
            </div>"""

        with st.spinner("Analysing fundus image…"):
            models       = load_all_models()
            model_results = predict_all(image_path)
            final_result  = ensemble_decision(model_results)
            report        = generate_text_explanation(final_result, model_results)

        st.markdown(f'<div class="card">{steps_html}</div>', unsafe_allow_html=True)

        # Detected conditions
        detected_diseases = [d[0] for d in final_result.get("detected_conditions", [])]
        confidence_map    = {d[0]: d[1] for d in final_result.get("detected_conditions", [])} if len(final_result.get("detected_conditions", [[]])[0]) > 1 else {}

        def conf_tag(name):
            conf = confidence_map.get(name, 1.0)
            if conf >= 0.75:   return "tag-high",   "HIGH"
            elif conf >= 0.45: return "tag-medium",  "MED"
            else:              return "tag-low",      "LOW"

        tags_html = '<div class="tag-row">'
        for d in detected_diseases:
            cls, label = conf_tag(d)
            tags_html += f'<span class="tag {cls}">{d} · {label}</span>'
        tags_html += '</div>'

        card_cls = "card-warning" if detected_diseases else "card-success"
        st.markdown(f"""
        <div class="card {card_cls}">
            <div class="card-label">Detected Conditions</div>
            {tags_html if detected_diseases else '<span style="color:#00e0a0;font-size:14px;">✓ No pathology detected</span>'}
        </div>
        """, unsafe_allow_html=True)

        # Diagnosis report
        st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-label" style="margin-bottom:12px;">Step 03 — Diagnosis Report</div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)

# ── XAI Section ───────────────────────────────────────────────────────────────
if uploaded_file is not None and detected_diseases:
    st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="xai-header">
        <div class="card-label" style="margin:0;">Step 04 — Explainability (Grad-CAM)</div>
        <span class="xai-count">{len(detected_diseases)} condition(s) visualised</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Generating Grad-CAM visualisations…"):
        explanations = generate_explanations(image_path, models, detected_diseases)

    cols = st.columns(min(len(explanations), 3), gap="medium")
    for i, (disease, data) in enumerate(explanations.items()):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="card" style="padding:20px 20px 12px;">
                <div class="card-label" style="margin-bottom:10px;">Grad-CAM · {disease}</div>
            """, unsafe_allow_html=True)
            st.image(data["image"], use_container_width=True)
            kw_html = " ".join(f'<span class="kw-pill">{k}</span>' for k in data["keywords"])
            st.markdown(f'<div style="margin-top:12px;">{kw_html}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding: 80px 0; color: #2a4060;">
        <div style="font-size:48px; margin-bottom:16px;">👁️</div>
        <div style="font-family:'DM Serif Display',serif; font-size:22px; color:#1a3055; margin-bottom:8px;">No image uploaded yet</div>
        <div style="font-size:13px; color:#1a2d42;">Upload a fundus photograph to begin AI-assisted diagnosis.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-content