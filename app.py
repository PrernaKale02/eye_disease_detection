import html
import os
import time
from pathlib import Path

import streamlit as st
from PIL import Image

from clinical_explainer import build_clinical_report
from ensemble import ensemble_decision
from explain import generate_explanations
from keywords_config import DISEASE_CONFIG
from load_models import load_all_models
from predict import predict_all

st.set_page_config(page_title="Retinal Disease Detection", page_icon="◉", layout="wide")
st.markdown("""
<style>
    :root {
        color-scheme: light;
        --page: #f3f7fb;
        --surface: #ffffff;
        --surface-subtle: #f7fafc;
        --border: #d9e4ee;
        --ink: #172b3f;
        --muted: #52677c;
        --blue: #1769aa;
        --teal: #087f8c;
        --teal-soft: #e7f5f4;
        --danger: #9b3e4a;
        --shadow: 0 12px 32px rgba(31, 58, 82, .08);
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        color: var(--ink);
    }

    .stApp {
        background:
            radial-gradient(ellipse at 85% 0, rgba(28, 128, 157, .08), transparent 34%),
            var(--page);
        color: var(--ink);
    }

    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent; }
    .block-container {
        max-width: 1320px;
        padding: 2rem 2.25rem 3rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
        padding: 1.8rem 2rem;
        border: 1px solid #d4e5ee;
        border-radius: 20px;
        background: linear-gradient(115deg, #ffffff 0%, #eef7fa 100%);
        box-shadow: var(--shadow);
    }
    .hero::after {
        position: absolute;
        top: -7rem;
        right: -3rem;
        width: 20rem;
        height: 20rem;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(25, 132, 157, .12), transparent 68%);
        content: "";
        pointer-events: none;
    }
    .eyebrow, .kicker {
        color: var(--teal);
        font-size: .7rem;
        font-weight: 750;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: .5rem 0 .4rem;
        color: #163650;
        font-size: clamp(1.8rem, 3vw, 2.35rem);
        font-weight: 750;
        line-height: 1.15;
    }
    .hero p {
        max-width: 48rem;
        margin: 0;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.6;
    }
    .hero-badge {
        float: right;
        padding: .45rem .75rem;
        border: 1px solid #bddbdc;
        border-radius: 999px;
        background: #f0f9f8;
        color: #12636d;
        font-size: .68rem;
        font-weight: 750;
        letter-spacing: .07em;
    }

    .panel {
        margin-bottom: 1rem;
        padding: 1.25rem 1.4rem;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: var(--shadow);
    }
    .tight { padding: 1.05rem 1.2rem; }
    .panel h2, .panel h3 {
        margin: .2rem 0 .5rem;
        color: #193a55;
        font-weight: 700;
        line-height: 1.3;
    }
    .panel h2 { font-size: 1.2rem; }
    .panel h3 { font-size: 1.05rem; }
    .muted {
        color: var(--muted);
        font-size: .9rem;
        line-height: 1.6;
    }
    .badge {
        display: inline-block;
        padding: .4rem .7rem;
        border: 1px solid #c8dbe8;
        border-radius: 999px;
        background: #f1f7fb;
        color: #28536e;
        font-size: .68rem;
        font-weight: 750;
        letter-spacing: .04em;
    }
    .good {
        border-color: #b8deda;
        background: var(--teal-soft);
        color: #155f5d;
    }
    .alert {
        border-color: #e5c6ca;
        background: #fff4f3;
        color: #813640;
    }
    .error-card {
        margin: 1rem 0;
        padding: 1.15rem 1.3rem;
        border: 1px solid #e5c6ca;
        border-left: 4px solid var(--danger);
        border-radius: 14px;
        background: #fff8f7;
        box-shadow: 0 5px 16px rgba(91, 42, 48, .05);
    }
    .error-card .kicker { color: var(--danger); }
    .error-card h3 {
        margin: .35rem 0 .45rem;
        color: #702e37;
        font-size: 1.05rem;
    }
    .error-card p {
        margin: .25rem 0 0;
        color: #704c50;
        font-size: .88rem;
        line-height: 1.55;
    }
    .error-card .error-next {
        color: #563f43;
        font-weight: 600;
    }

    .result {
        margin: 1rem 0;
        padding: 1.5rem;
        border: 1px solid #b8deda;
        border-radius: 18px;
        background: linear-gradient(120deg, #f0faf7, #ffffff 72%);
        box-shadow: var(--shadow);
    }
    .result.disease {
        border-color: #e4c5c8;
        background: linear-gradient(120deg, #fff6f4, #ffffff 72%);
    }
    .result-name {
        margin: .45rem 0;
        color: #193c54;
        font-size: clamp(1.55rem, 3vw, 2rem);
        font-weight: 750;
        line-height: 1.2;
    }
    .result-desc {
        color: var(--muted);
        font-size: .95rem;
        line-height: 1.5;
    }
    .confidence-row {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 1.2rem;
    }
    .confidence {
        color: #155f70;
        font-size: 1.8rem;
        font-weight: 750;
    }
    .stat-label {
        color: var(--muted);
        font-size: .68rem;
        font-weight: 750;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .meter {
        height: 8px;
        margin-top: .65rem;
        overflow: hidden;
        border-radius: 99px;
        background: #e4edf2;
    }
    .meter span {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #247caf, #159b91);
    }
    .result-note { margin-top: 1rem; }
    .section-label { margin: 1.5rem 0 .65rem; }

    .model-card {
        height: 100%;
        min-height: 120px;
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: var(--surface);
        box-shadow: 0 5px 16px rgba(31, 58, 82, .05);
    }
    .model-title {
        margin-bottom: .45rem;
        color: var(--muted);
        font-size: .78rem;
        font-weight: 650;
        line-height: 1.4;
    }
    .model-pred {
        min-height: 1.5rem;
        color: #193a55;
        font-size: .98rem;
        font-weight: 750;
        overflow-wrap: anywhere;
    }
    .model-prob {
        margin-top: .55rem;
        color: var(--muted);
        font-size: .72rem;
        line-height: 1.4;
    }
    .small-note {
        color: var(--muted);
        font-size: .75rem;
        line-height: 1.55;
    }
    .caption {
        margin: .45rem 0 .8rem;
        color: var(--muted);
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-align: center;
        text-transform: uppercase;
    }
    .progress-panel {
        margin: 1.25rem 0 1.5rem;
        padding: 1.05rem 1.25rem;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: var(--shadow);
    }
    .progress-steps {
        display: flex;
        align-items: flex-start;
        margin: 0;
        padding: 0;
        list-style: none;
    }
    .progress-step {
        position: relative;
        display: flex;
        flex: 1;
        flex-direction: column;
        align-items: center;
        gap: .45rem;
        color: #738598;
        text-align: center;
    }
    .progress-step:not(:last-child)::after {
        position: absolute;
        top: 15px;
        left: calc(50% + 17px);
        width: calc(100% - 34px);
        height: 2px;
        border-radius: 2px;
        background: #dce6ed;
        content: "";
    }
    .progress-step.complete:not(:last-child)::after { background: #65aaa6; }
    .progress-node {
        z-index: 1;
        display: grid;
        width: 32px;
        height: 32px;
        place-items: center;
        border: 1px solid #ccd8e1;
        border-radius: 50%;
        background: #f5f8fa;
        color: #65798c;
        font-size: .78rem;
        font-weight: 750;
    }
    .progress-label {
        color: inherit;
        font-size: .8rem;
        font-weight: 650;
        line-height: 1.3;
    }
    .progress-step.active { color: var(--teal); }
    .progress-step.active .progress-node {
        border-color: var(--teal);
        background: var(--teal);
        color: #ffffff;
        box-shadow: 0 0 0 4px var(--teal-soft);
    }
    .progress-step.complete { color: #286f6c; }
    .progress-step.complete .progress-node {
        border-color: #65aaa6;
        background: #e7f5f4;
        color: #286f6c;
    }

    [data-testid="stFileUploader"] {
        padding: .85rem;
        border: 1px dashed #93b8c9;
        border-radius: 14px;
        background: #f7fbfd;
    }
    [data-testid="stFileUploader"]:hover { border-color: var(--blue); }
    [data-testid="stFileUploader"] label { color: #294b63; }
    [data-testid="stImage"] img {
        max-width: 100%;
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    button {
        border-radius: 9px !important;
        font-weight: 650 !important;
    }
    button:focus-visible, input:focus-visible, summary:focus-visible,
    [role="button"]:focus-visible {
        outline: 3px solid #2384b5 !important;
        outline-offset: 3px !important;
    }
    div[role="alert"] {
        border: 1px solid #e5c6ca;
        border-radius: 12px;
        background: #fff4f3;
        color: #702e37;
    }
    .stSpinner > div { border-top-color: var(--teal); }
    details {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: var(--surface);
    }
    details summary { color: #193a55; font-weight: 650; }
    .footer {
        margin-top: 1.5rem;
        padding: 1rem .5rem .2rem;
        border-top: 1px solid var(--border);
        color: var(--muted);
        font-size: .75rem;
        line-height: 1.7;
        text-align: center;
    }

    @media (max-width: 800px) {
        .block-container { padding: 1rem .9rem 2rem; }
        .hero { padding: 1.25rem; border-radius: 16px; }
        .hero-badge {
            float: none;
            display: inline-block;
            margin-bottom: .7rem;
        }
        .panel { padding: 1rem; }
        .tight { padding: .9rem; }
        .result { padding: 1.15rem; }
    }
    @media (max-width: 480px) {
        .progress-panel { padding: .9rem .55rem; }
        .progress-step { gap: .4rem; }
        .progress-step:not(:last-child)::after {
            top: 14px;
            left: calc(50% + 15px);
            width: calc(100% - 30px);
        }
        .progress-node { width: 30px; height: 30px; }
        .progress-label { font-size: .68rem; }
        .confidence-row { align-items: flex-start; flex-direction: column; }
        .hero p { font-size: .9rem; }
    }
</style>""", unsafe_allow_html=True)

def progress_markup(active_step):
    labels = ("Upload Image", "Analyze Image", "View Results")
    steps = []
    for number, label in enumerate(labels, start=1):
        state = "complete" if number < active_step else "active" if number == active_step else "upcoming"
        current = ' aria-current="step"' if number == active_step else ""
        steps.append(
            f'<li class="progress-step {state}"{current}>'
            f'<span class="progress-node">{number}</span>'
            f'<span class="progress-label">{label}</span></li>'
        )
    return (
        '<div class="progress-panel"><ol class="progress-steps" '
        'aria-label="Analysis progress">'
        f'{"".join(steps)}</ol></div>'
    )

def show_error(title, message, next_step, exception):
    st.markdown(
        f'<div class="error-card" role="alert">'
        f'<div class="kicker">Unable to continue</div>'
        f'<h3>{html.escape(title)}</h3>'
        f'<p>{html.escape(message)}</p>'
        f'<p class="error-next">Next step: {html.escape(next_step)}</p></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Technical details (for developers)"):
        st.exception(exception)

st.markdown('<header class="hero" aria-labelledby="page-title"><span class="hero-badge">CLINICAL AI · OPHTHALMOLOGY</span><div class="eyebrow">Retinal imaging · Explainable prediction</div><h1 id="page-title">Retinal Disease Detection</h1><p>AI-powered retinal image analysis with explainable predictions. Explore model outputs and visual attention from a fundus photograph.</p></header>', unsafe_allow_html=True)

progress_display = st.empty()
left, right = st.columns([1, 1.38], gap="medium")
with left:
    st.markdown('<div class="panel"><div class="kicker">01 · Image input</div><h2>Upload Fundus Image</h2><div class="muted">Upload a retinal fundus image to begin automated analysis.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a JPG or PNG fundus image", type=["jpg", "jpeg", "png"])
    st.markdown('<div class="small-note">Accepted: JPG, JPEG, PNG · Inference resolution: 224 × 224</div></div>', unsafe_allow_html=True)

progress_display.markdown(
    progress_markup(2 if uploaded else 1),
    unsafe_allow_html=True,
)

with right:
    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
        except Exception as exc:
            show_error(
                "This image could not be opened",
                "The selected file could not be read as an image.",
                "Choose a valid JPG or PNG image and try again.",
                exc,
            )
            st.stop()
        st.markdown('<div class="panel tight"><div class="kicker">Image preview</div><h3>Ready for analysis</h3>', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown(f'<span class="badge good">IMAGE READY</span> <span class="small-note">{html.escape(uploaded.name)} · {image.width} × {image.height} px</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="panel tight"><div class="kicker">Image preview</div><h3>Ready when you are</h3><div class="muted">Your preview and image dimensions will appear here after upload.</div><div style="height:115px"></div></div>', unsafe_allow_html=True)

if uploaded is None:
    st.markdown('<div class="footer">Retinal Disease Detection · Explainable AI<br>Research / Educational Prototype — Not a Medical Diagnostic Device</div>', unsafe_allow_html=True)
    st.stop()

os.makedirs("temp", exist_ok=True)
suffix = Path(uploaded.name).suffix.lower() or ".jpg"
image_path = os.path.join("temp", f"streamlit_upload_{hash(uploaded.getvalue()) & 0xffffffff:08x}{suffix}")
with open(image_path, "wb") as target:
    target.write(uploaded.getbuffer())

st.markdown('<div class="panel tight"><div class="kicker">02 · Model inference</div><h3>Analyzing retinal image…</h3><div class="muted">Running the disease models and combining their outputs.</div>', unsafe_allow_html=True)
started = time.perf_counter()
try:
    with st.spinner("Running ensemble models"):
        models = load_all_models()
        model_results = predict_all(image_path)
        final_result = ensemble_decision(model_results)
    elapsed = time.perf_counter() - started
    progress_display.markdown(progress_markup(3), unsafe_allow_html=True)
    st.markdown(f'<span class="badge good">ANALYSIS COMPLETE</span> <span class="small-note">Inference finished in {elapsed:.1f} seconds</span></div>', unsafe_allow_html=True)
except Exception as exc:
    show_error(
        "Image analysis failed",
        "The application could not complete the model analysis. This may be due to unavailable model files or another processing issue.",
        "Confirm the required model files are present and configured, then try again. If the problem continues, share the technical details with the application maintainer.",
        exc,
    )
    st.stop()

detected = final_result.get("detected_conditions", [])
most_likely = final_result.get("most_likely_disease", "No disease detected")
has_disease = bool(detected)
top_conf = float(detected[0][1]) if detected else None
result_cls = "disease" if has_disease else ""
result_label = "DISEASE DETECTED" if has_disease else "NORMAL"
result_desc = most_likely if has_disease else "No retinal disease detected by the ensemble."
st.markdown(f'<div class="result {result_cls}"><div class="kicker">AI diagnosis · {result_label}</div><div class="result-name">{html.escape(result_desc)}</div><div class="result-desc">{"Ensemble-selected condition" if has_disease else "No conditions crossed the ensemble detection thresholds."}</div>', unsafe_allow_html=True)
if top_conf is not None:
    st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:end;margin-top:19px"><div><div class="stat-label">Ensemble confidence</div><div class="confidence">{top_conf:.1%}</div></div><span class="badge alert">REVIEW WITH A PROFESSIONAL</span></div><div class="meter"><span style="width:{max(0,min(top_conf,1)):.1%}"></span></div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="margin-top:16px"><span class="badge good">NO DETECTED CONDITION</span><div class="small-note" style="margin-top:8px">No single ensemble confidence is produced for a normal result. See model outputs below.</div></div></div>', unsafe_allow_html=True)

st.markdown('<div class="kicker" style="margin:22px 0 9px">03 · Model analysis</div>', unsafe_allow_html=True)
def predicted_confidence(result, key):
    raw, prediction = float(result["confidence"]), result["prediction"]
    if key in ("glaucoma", "cataract"):
        return 1 - raw if prediction in ("Glaucoma", "Cataract") else raw
    if key == "dme":
        return raw if prediction == "DME_Present" else 1 - raw
    return raw # DR confidence is the maximum predicted class probability.

specs = [("DR · ResNet50", "dr"), ("DME · EfficientNet-B3", "dme"), ("Glaucoma · EfficientNetB0", "glaucoma"), ("Cataract · EfficientNetB0", "cataract")]
cards = st.columns(4, gap="small")
for col, (label, key) in zip(cards, specs):
    item = model_results[key]
    conf = max(0.0, min(predicted_confidence(item, key), 1.0))
    with col:
        st.markdown(f'<div class="model-card"><div class="model-title">{html.escape(label)}</div><div class="model-pred">{html.escape(str(item["prediction"]))}</div><div class="model-prob">Predicted class confidence · {conf:.1%}</div><div class="meter"><span style="width:{conf:.1%}"></span></div></div>', unsafe_allow_html=True)

st.markdown(f'<div class="panel tight"><div class="kicker">04 · Ensemble decision</div><h3>Final condition: {html.escape(most_likely)}</h3><div class="muted">The existing ensemble applies configured disease thresholds, ranks detected conditions by confidence, and applies its DR + DME selection rule when applicable.</div></div>', unsafe_allow_html=True)

if detected:
    st.markdown('<div class="kicker" style="margin:20px 0 9px">05 · Prediction details</div>', unsafe_allow_html=True)
    details = st.columns(min(len(detected), 2), gap="medium")
    for index, (disease, confidence) in enumerate(detected):
        config = DISEASE_CONFIG[disease]
        output = model_results[config["model_key"]]
        clinical = build_clinical_report(disease, output["prediction"], output["confidence"], [])
        with details[index % len(details)]:
            with st.expander(f"{disease} · {confidence:.1%} ensemble confidence", expanded=index == 0):
                st.markdown(f'**Stage:** {html.escape(str(clinical["stage"]))}  \n**Risk:** {html.escape(str(clinical["risk"]))}')
                st.write(clinical["explanation"])
                st.write(clinical["advice"])

    st.markdown('<div class="kicker" style="margin:20px 0 9px">06 · Explainability</div><div class="panel tight"><h2>Explainable AI</h2><div class="muted">Visual explanation of regions influencing the model prediction. Highlighted regions represent areas that contributed most strongly to the selected prediction.</div></div>', unsafe_allow_html=True)
    try:
        with st.spinner("Generating Grad-CAM visualizations"):
            explanations = generate_explanations(image_path, models, [name for name, _ in detected])
        if not explanations:
            st.info("Grad-CAM did not return visualizations for the detected conditions.")
        for disease, data in explanations.items():
            st.markdown(f'<div class="panel tight"><div class="kicker">Grad-CAM · {html.escape(disease)}</div><h3>Model attention overlay</h3>', unsafe_allow_html=True)
            orig, overlay = st.columns(2, gap="medium")
            with orig:
                st.image(image, use_container_width=True)
                st.markdown('<div class="caption">Original fundus image</div>', unsafe_allow_html=True)
            with overlay:
                st.image(data["image"], use_container_width=True)
                st.markdown('<div class="caption">Grad-CAM overlay</div>', unsafe_allow_html=True)
            if data.get("keywords"):
                st.markdown("**Activation cues:** " + " · ".join(html.escape(str(value)) for value in data["keywords"]))
            st.markdown('<div class="small-note">The current Grad-CAM function returns an overlay; it does not expose a standalone heatmap image.</div></div>', unsafe_allow_html=True)
    except Exception as exc:
        show_error(
            "Visual explanation could not be generated",
            "The prediction is available, but the optional Grad-CAM visualization failed.",
            "Review the prediction above. If you need the visual explanation, share the technical details with the application maintainer.",
            exc,
        )

with st.expander("Technical Details"):
    st.markdown("**Models:** ResNet50 (DR), EfficientNet-B3 (DME), EfficientNetB0 (Glaucoma and Cataract)  \n**Input resolution:** 224 × 224 pixels  \n**Ensemble:** configured thresholds, confidence ranking, DR + DME rule  \n**Explainability:** TensorFlow Grad-CAM and PyTorch Grad-CAM for detected conditions  \n**Framework:** Streamlit, TensorFlow/Keras, PyTorch, OpenCV  \n**Processing:** Complete")
st.markdown('<div class="footer">Retinal Disease Detection · Explainable AI<br>Research / Educational Prototype — Not a Medical Diagnostic Device. This system is intended for research and education and should not replace professional medical diagnosis.</div>', unsafe_allow_html=True)
