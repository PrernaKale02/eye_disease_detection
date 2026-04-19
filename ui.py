import streamlit as st
import os

from load_models import load_all_models
from predict import predict_all
from ensemble import ensemble_decision
from explain import generate_explanations
from feature_extraction import generate_text_explanation
from clinical_explainer import build_clinical_report
from keywords_config import DISEASE_CONFIG


# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(
    page_title="RetinaScan AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------
# Styles
# ------------------------------------------------
st.markdown("""
<style>

.stApp{
    background:#050d1a;
    color:#e8edf5;
}

.hero{
    padding:50px 60px;
    background:linear-gradient(135deg,#060f20,#0a1a35,#061428);
    border-bottom:1px solid #1a2d50;
}

.hero-title{
    font-size:42px;
    font-weight:500;
}

.hero-title span{
    color:#00b4ff;
}

.main-content{
    padding:40px 60px;
}

.card{
    background:#0a1628;
    border:1px solid #1a2d50;
    border-radius:10px;
    padding:24px;
    margin-bottom:20px;
}

.tag{
    border-radius:20px;
    padding:4px 12px;
    font-size:12px;
    border:1px solid;
}

.tag-high{
    color:#ff6b6b;
    border-color:#ff6b6b;
}

.tag-medium{
    color:#ffb347;
    border-color:#ffb347;
}

.tag-low{
    color:#00e0a0;
    border-color:#00e0a0;
}

.kw-pill{
    background:#0f1e35;
    border:1px solid #1a3055;
    border-radius:6px;
    padding:4px 10px;
    margin:4px;
    font-size:12px;
    display:inline-block;
}

.report-box{
    background:#060f1e;
    border:1px solid #1a2d50;
    border-radius:8px;
    padding:20px;
    font-family:monospace;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Hero Header
# ------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">Retina<span>Scan</span> AI</div>
    <div>Deep-learning ensemble analysis for automated retinal disease detection.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ------------------------------------------------
# Upload Section
# ------------------------------------------------
col1, col2 = st.columns([1,1.5])

with col1:

    st.markdown('<div class="card">Upload Fundus Image</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload JPG / PNG fundus image",
        type=["jpg","png","jpeg"]
    )

    if uploaded_file is not None:

        os.makedirs("temp", exist_ok=True)

        image_path = os.path.join("temp", uploaded_file.name)

        with open(image_path,"wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(image_path, use_container_width=True)


# ------------------------------------------------
# Analysis Section
# ------------------------------------------------
with col2:

    if uploaded_file is not None:

        with st.spinner("Running AI analysis..."):

            models = load_all_models()

            model_results = predict_all(image_path)

            final_result = ensemble_decision(model_results)

            report = generate_text_explanation(final_result, model_results)

        # ------------------------------------------------
        # Diagnosis Report
        # ------------------------------------------------
        st.markdown('<div class="card">Diagnosis Report</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)

        # ------------------------------------------------
        # Detected Conditions
        # ------------------------------------------------
        detected_diseases = [d[0] for d in final_result["detected_conditions"]]

        confidence_map = {d[0]:d[1] for d in final_result["detected_conditions"]}

        tag_html = ""

        for d in detected_diseases:

            conf = confidence_map[d]

            if conf >= 0.75:
                cls="tag-high"
            elif conf >= 0.45:
                cls="tag-medium"
            else:
                cls="tag-low"

            tag_html += f'<span class="tag {cls}">{d} ({conf:.2f})</span> '

        st.markdown(f'<div class="card">{tag_html}</div>', unsafe_allow_html=True)


# ------------------------------------------------
# GradCAM Section
# ------------------------------------------------
if uploaded_file is not None and detected_diseases:

    st.markdown("## Explainable AI Analysis")

    explanations = generate_explanations(
        image_path,
        models,
        detected_diseases
    )

    cols = st.columns(min(len(explanations),3))

    for i,(disease,data) in enumerate(explanations.items()):

        with cols[i % len(cols)]:

            keywords = data["keywords"]

            prediction = model_results[
                DISEASE_CONFIG[disease]["model_key"]
            ]["prediction"]

            confidence = model_results[
                DISEASE_CONFIG[disease]["model_key"]
            ]["confidence"]

            clinical = build_clinical_report(
                disease,
                prediction,
                confidence,
                keywords
            )

            st.markdown(f'<div class="card">Grad-CAM · {disease}</div>', unsafe_allow_html=True)

            st.image(data["image"], use_container_width=True)

            # Keywords
            kw_html = "".join([f'<span class="kw-pill">{k}</span>' for k in keywords])

            st.markdown(kw_html, unsafe_allow_html=True)

            # Clinical Analysis
            st.markdown(f"""
            **Stage:** {clinical["stage"]}  
            **Risk Level:** {clinical["risk"]}

            **Explanation:**  
            {clinical["explanation"]}

            **Clinical Recommendation:**  
            {clinical["advice"]}
            """)

# ------------------------------------------------
# Empty State
# ------------------------------------------------
elif uploaded_file is None:

    st.markdown("""
    <div style="text-align:center;padding:80px;">
        <h2>No image uploaded</h2>
        Upload a fundus photograph to begin analysis.
    </div>
    """, unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)