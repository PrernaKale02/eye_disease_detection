DR_THRESHOLD = 0.6
DME_THRESHOLD = 0.5
GLAUCOMA_THRESHOLD = 0.6
CATARACT_THRESHOLD = 0.6


def ensemble_decision(results):

    detected = []

    # ---------------- DR ----------------
    dr_pred = results["dr"]["prediction"]
    dr_conf = results["dr"]["confidence"]

    if dr_pred != "No_DR" and dr_conf > DR_THRESHOLD:
        detected.append(("Diabetic Retinopathy", dr_conf))

    # ---------------- DME ----------------
    dme_prob = results["dme"]["confidence"]

    if dme_prob > DME_THRESHOLD:
        detected.append(("Diabetic Macular Edema", dme_prob))

    # ---------------- Glaucoma ----------------
    glaucoma_norm_prob = results["glaucoma"]["confidence"]
    glaucoma_prob = 1 - glaucoma_norm_prob

    if glaucoma_prob > GLAUCOMA_THRESHOLD:
        detected.append(("Glaucoma", glaucoma_prob))

    # ---------------- Cataract ----------------
    cataract_norm_prob = results["cataract"]["confidence"]
    cataract_prob = 1 - cataract_norm_prob

    if cataract_prob > CATARACT_THRESHOLD:
        detected.append(("Cataract", cataract_prob))

    # ---------------- Most likely disease ----------------
    if detected:
        most_likely = max(detected, key=lambda x: x[1])[0]
    else:
        most_likely = "No disease detected"

    detected = sorted(detected, key=lambda x: x[1], reverse=True)
    
    return {
        "most_likely_disease": detected[0][0] if detected else "None",
        "detected_conditions": detected
    }