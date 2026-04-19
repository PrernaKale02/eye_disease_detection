import streamlit as st
import cv2
import os

from load_models import load_all_models
from predict import predict_all
from ensemble import ensemble_decision
from explain import generate_explanations
from feature_extraction import generate_text_explanation


st.title("Retinal Disease Detection System")

uploaded_file = st.file_uploader(
    "Upload a fundus image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:

    image_path = os.path.join("test_images", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Fundus Image", use_container_width=True)

    st.write("Running AI analysis...")

    models = load_all_models()

    model_results = predict_all(image_path)

    final_result = ensemble_decision(model_results)

    report = generate_text_explanation(final_result, model_results)

    st.subheader("Diagnosis Report")
    st.text(report)

    detected_diseases = [d[0] for d in final_result["detected_conditions"]]

    explanations = generate_explanations(
        image_path,
        models,
        detected_diseases
    )

    st.subheader("Explainable AI Visualizations")

    for disease, data in explanations.items():

        img = data["image"]
        keywords = data["keywords"]

        st.image(img, caption=f"{disease} Grad-CAM")

        st.write("Detected features:")
        for k in keywords:
            st.write(f"• {k}")