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
    # determine most likely disease
    disease_names = [d[0] for d in detected]

    # ---------------- Special DR + DME rule ----------------
    dr_conf = None
    dme_conf = None

    for d, conf in detected:
        if d == "Diabetic Retinopathy":
            dr_conf = conf
        if d == "Diabetic Macular Edema":
            dme_conf = conf

    # Apply rule only if DR and DME are the only diseases detected
    if (
        dr_conf is not None
        and dme_conf is not None
        and len(detected) == 2
        and dme_conf >= 0.60
    ):
        most_likely = "Diabetic Macular Edema"

    elif detected:
        most_likely = max(detected, key=lambda x: x[1])[0]

    else:
        most_likely = "No disease detected"
    detected = sorted(detected, key=lambda x: x[1], reverse=True)
    
    return {
        "most_likely_disease": most_likely,
        "detected_conditions": detected
    }