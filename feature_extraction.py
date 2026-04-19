def generate_text_explanation(final_result, model_results):

    most_likely = final_result["most_likely_disease"]
    detected = final_result["detected_conditions"]

    explanation = []

    explanation.append("Diagnosis Report")
    explanation.append("----------------")

    explanation.append(f"Most likely disease: {most_likely}")
    explanation.append("")

    if detected:
        explanation.append("Detected conditions:")

        for disease, conf in detected:
            explanation.append(f"• {disease} (confidence: {conf:.2f})")

    else:
        explanation.append("No retinal diseases detected.")

    explanation.append("")
    explanation.append("Explanation:")

    detected_names = [d[0] for d in detected]

    # ---------------- Special DR + DME explanation ----------------
    if "Diabetic Retinopathy" in detected_names and "Diabetic Macular Edema" in detected_names:

        explanation.append(
            "Diabetic Macular Edema (DME) has been detected as a complication of Diabetic Retinopathy. "
            "DME occurs when damaged retinal blood vessels caused by diabetic retinopathy leak fluid "
            "into the macula, the central part of the retina responsible for sharp vision."
        )

    # ---------------- Individual disease explanations ----------------

    if "Glaucoma" in detected_names:
        explanation.append(
            "Grad-CAM highlights regions around the optic disc, suggesting structural patterns associated with glaucoma."
        )

    if "Diabetic Macular Edema" in detected_names:
        explanation.append(
            "Highlighted regions near the macula indicate fluid accumulation patterns consistent with diabetic macular edema."
        )

    if "Diabetic Retinopathy" in detected_names:
        explanation.append(
            "The model identified retinal lesion patterns such as microaneurysms or hemorrhage-like structures associated with diabetic retinopathy."
        )

    if "Cataract" in detected_names:
        explanation.append(
            "Opacity-related visual patterns detected by the model suggest the presence of cataract."
        )

    return "\n".join(explanation)

import numpy as np
def extract_keywords_from_heatmap(heatmap, disease):

    h, w = heatmap.shape

    left = heatmap[:, :w//3]
    center = heatmap[:, w//3:2*w//3]
    right = heatmap[:, 2*w//3:]

    left_score = np.mean(left)
    center_score = np.mean(center)
    right_score = np.mean(right)

    keywords = []

    if disease == "Glaucoma":

        if max(left_score, right_score) > 0.15:
            keywords.append("optic disc region activation")

    elif disease == "Diabetic Macular Edema":

        if center_score > 0.12:
            keywords.append("macular region abnormality")

    elif disease == "Diabetic Retinopathy":

        if np.mean(heatmap) > 0.08:
            keywords.append("possible retinal lesion patterns")

    elif disease == "Cataract":

        keywords.append("global opacity pattern detected")

    if not keywords:
        keywords.append("retinal activation pattern detected")

    return keywords