import cv2

from load_models import load_all_models
from predict import predict_all
from ensemble import ensemble_decision
from explain import generate_explanations
from feature_extraction import generate_text_explanation
from clinical_explainer import build_clinical_report
from keywords_config import DISEASE_CONFIG


# ------------------------------------------------
# Load models once
# ------------------------------------------------
models = load_all_models()

# ------------------------------------------------
# Input image
# ------------------------------------------------
image_path = "sample_glaucoma.jpg"

# ------------------------------------------------
# Run predictions
# ------------------------------------------------
model_results = predict_all(image_path)

print("Model outputs:")
print(model_results)

# ------------------------------------------------
# Ensemble decision
# ------------------------------------------------
final_result = ensemble_decision(model_results)

print("\nFinal diagnosis:")
print(final_result)

report = generate_text_explanation(final_result, model_results)

print("\n")
print(report)

# ------------------------------------------------
# Extract disease names (remove confidence values)
# ------------------------------------------------
detected_diseases = [d[0] for d in final_result["detected_conditions"]]

# ------------------------------------------------
# Generate Grad-CAM explanations
# ------------------------------------------------
explanations = generate_explanations(
    image_path,
    models,
    detected_diseases
)

print("\nClinical Analysis\n----------------")

for disease, data in explanations.items():

    keywords = data["keywords"]

    prediction = model_results[DISEASE_CONFIG[disease]["model_key"]]["prediction"]

    confidence = model_results[DISEASE_CONFIG[disease]["model_key"]]["confidence"]

    report = build_clinical_report(
        disease,
        prediction,
        confidence,
        keywords
    )

    print(f"\nDisease: {report['disease']}")
    print(f"Stage: {report['stage']}")
    print(f"Risk Level: {report['risk']}")
    print("\nExplanation:")
    print(report["explanation"])

    print("\nClinical Recommendation:")
    print(report["advice"])

# ------------------------------------------------
# Save Grad-CAM images
# ------------------------------------------------
for disease, data in explanations.items():

    img = data["image"]
    keywords = data["keywords"]
    features = keywords if keywords else ["retinal region activation detected"]

    output_path = f"outputs/{disease}_gradcam.jpg"

    cv2.imwrite(output_path, img)

    print(f"\n{disease} explanation:")
    print("Detected features:")

    for k in keywords:
        print(f"• {k}")