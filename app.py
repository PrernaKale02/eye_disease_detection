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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--bg:#07111f;--panel:#0c1a2c;--line:#20344c;--text:#e8f0fa;--muted:#91a4bb;--cyan:#46c8e8}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:radial-gradient(ellipse at 78% -12%,rgba(27,123,167,.18),transparent 38%),var(--bg);color:var(--text)}
#MainMenu,footer{visibility:hidden}.block-container{max-width:1420px;padding:1.15rem 2.2rem 2rem}[data-testid="stHeader"]{background:transparent}
.hero{padding:22px 26px 20px;border:1px solid rgba(96,174,212,.2);border-radius:18px;background:linear-gradient(110deg,#0e2338,#0a1829);margin-bottom:20px;position:relative;overflow:hidden}.hero:after{content:'';position:absolute;right:-55px;top:-110px;width:300px;height:300px;background:radial-gradient(circle,rgba(70,200,232,.14),transparent 68%);pointer-events:none}.eyebrow,.kicker{font-size:10px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--cyan)}
.hero h1{font:800 clamp(25px,3vw,36px)/1.15 Manrope,sans-serif;margin:8px 0 6px;color:#f3f8ff}.hero p{color:#a7b8cc;font-size:14px;margin:0;max-width:730px}.hero-badge{float:right;border:1px solid #2b5269;border-radius:999px;padding:7px 11px;color:#a9dced;font-size:10px;letter-spacing:1px;font-weight:700;background:#10283a}
.panel{background:linear-gradient(145deg,#0e1d2f,#0a1625);border:1px solid var(--line);border-radius:15px;padding:18px 20px;box-shadow:0 10px 28px #0002;margin-bottom:14px}.tight{padding:15px 17px}.panel h2,.panel h3{font-family:Manrope,sans-serif;color:#edf5ff;margin:2px 0 7px}.panel h2{font-size:18px}.panel h3{font-size:15px}.muted{color:var(--muted);font-size:13px;line-height:1.55}.badge{display:inline-block;padding:5px 10px;border:1px solid #31516b;border-radius:999px;background:#10283a;color:#b6e7f4;font-size:10px;font-weight:700;letter-spacing:.5px}.good{color:#b9f1dc;border-color:#28624f;background:#102b27}.alert{color:#ffd8d9;border-color:#71424a;background:#301d26}
.result{border-radius:16px;padding:22px 24px;border:1px solid #28624f;background:linear-gradient(120deg,#0d2f27,#0c1d2a);margin:14px 0}.result.disease{border-color:#71464b;background:linear-gradient(120deg,#341d25,#131d2b)}.result-name{font:800 clamp(23px,3vw,32px)/1.15 Manrope,sans-serif;margin:7px 0;color:#f4f8fd}.result-desc{font-size:14px;color:#b8c8d9}.confidence{font:800 28px Manrope,sans-serif;color:#edfaff}.stat-label{color:#91a6bd;font-size:10px;text-transform:uppercase;letter-spacing:1.2px;font-weight:700}.meter{height:6px;border-radius:99px;background:#1b2a3b;margin-top:9px;overflow:hidden}.meter span{height:100%;display:block;border-radius:99px;background:linear-gradient(90deg,#39a9d5,#69dfce)}
.model-card{height:100%;min-height:120px;background:#0a1727;border:1px solid #1b3047;border-radius:12px;padding:14px}.model-title{font-size:12px;color:#a5b8cc;margin-bottom:7px}.model-pred{font-weight:700;font-size:15px;color:#eef5fd;min-height:23px}.model-prob{font-size:11px;color:var(--muted);margin-top:8px}.small-note{font-size:11px;color:#93a8bd;line-height:1.5}.caption{font-size:10px;text-align:center;text-transform:uppercase;letter-spacing:1px;color:#8da5bc;margin:5px 0 10px}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#31a6d7,#62d6c7)}[data-testid="stFileUploader"]{background:#091727;border:1px dashed #36536b;border-radius:12px;padding:12px}[data-testid="stFileUploader"]:hover{border-color:var(--cyan)}[data-testid="stFileUploader"] label{color:#c6d4e2}[data-testid="stImage"] img{border-radius:12px;border:1px solid #243b53}.stSpinner>div{border-top-color:var(--cyan)}div[data-testid="stExpander"]{border:1px solid var(--line);border-radius:12px;background:#0b1929}.footer{text-align:center;border-top:1px solid #1b2c40;padding:16px 8px 2px;color:#8298af;font-size:11px;line-height:1.7;margin-top:20px}
@media(max-width:800px){.block-container{padding:.7rem .8rem 1.5rem}.hero{padding:18px}.hero-badge{float:none;display:inline-block;margin-bottom:6px}.panel{padding:15px}}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="hero"><span class="hero-badge">CLINICAL AI · OPHTHALMOLOGY</span><div class="eyebrow">Retinal imaging · Explainable prediction</div><h1>Retinal Disease Detection</h1><p>AI-powered retinal image analysis with explainable predictions. Explore model outputs and visual attention from a fundus photograph.</p></div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.38], gap="medium")
with left:
    st.markdown('<div class="panel"><div class="kicker">01 · Image input</div><h2>Upload Fundus Image</h2><div class="muted">Upload a retinal fundus image to begin automated analysis.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a JPG or PNG fundus image", type=["jpg", "jpeg", "png"])
    st.markdown('<div class="small-note">Accepted: JPG, JPEG, PNG · Inference resolution: 224 × 224</div></div>', unsafe_allow_html=True)
with right:
    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
        except Exception as exc:
            st.error("This image could not be opened. Please upload a valid JPG or PNG.")
            st.exception(exc)
            st.stop()
        st.markdown('<div class="panel tight"><div class="kicker">Image preview</div><h3>Ready for analysis</h3>', unsafe_allow_html=True)
        st.image(image, width=360)
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
    st.markdown(f'<span class="badge good">ANALYSIS COMPLETE</span> <span class="small-note">Inference finished in {elapsed:.1f} seconds</span></div>', unsafe_allow_html=True)
except Exception as exc:
    st.error("Analysis could not be completed. Check that all model files are available and compatible.")
    st.exception(exc)
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
                st.image(image, width=360)
                st.markdown('<div class="caption">Original fundus image</div>', unsafe_allow_html=True)
            with overlay:
                st.image(data["image"], width=360)
                st.markdown('<div class="caption">Grad-CAM overlay</div>', unsafe_allow_html=True)
            if data.get("keywords"):
                st.markdown("**Activation cues:** " + " · ".join(html.escape(str(value)) for value in data["keywords"]))
            st.markdown('<div class="small-note">The current Grad-CAM function returns an overlay; it does not expose a standalone heatmap image.</div></div>', unsafe_allow_html=True)
    except Exception as exc:
        st.warning("Grad-CAM could not be generated for this result. The prediction remains available above.")
        st.exception(exc)

with st.expander("Technical Details"):
    st.markdown("**Models:** ResNet50 (DR), EfficientNet-B3 (DME), EfficientNetB0 (Glaucoma and Cataract)  \n**Input resolution:** 224 × 224 pixels  \n**Ensemble:** configured thresholds, confidence ranking, DR + DME rule  \n**Explainability:** TensorFlow Grad-CAM and PyTorch Grad-CAM for detected conditions  \n**Framework:** Streamlit, TensorFlow/Keras, PyTorch, OpenCV  \n**Processing:** Complete")
st.markdown('<div class="footer">Retinal Disease Detection · Explainable AI<br>Research / Educational Prototype — Not a Medical Diagnostic Device. This system is intended for research and education and should not replace professional medical diagnosis.</div>', unsafe_allow_html=True)
