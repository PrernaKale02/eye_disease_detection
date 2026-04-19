from keywords_config import DISEASE_CONFIG


# mapping from your model outputs → config class ids
DR_CLASS_MAP = {
    "No_DR": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
    "Proliferative": 4
}

DME_CLASS_MAP = {
    "No_DME": 0,
    "DME_Present": 2
}

GLAUCOMA_CLASS_MAP = {
    "Normal": 0,
    "Glaucoma": 1
}

CATARACT_CLASS_MAP = {
    "Normal": 0,
    "Cataract": 1
}


def get_class_id(disease, prediction):

    if disease == "Diabetic Retinopathy":
        return DR_CLASS_MAP.get(prediction, 0)

    if disease == "Diabetic Macular Edema":
        return DME_CLASS_MAP.get(prediction, 0)

    if disease == "Glaucoma":
        return GLAUCOMA_CLASS_MAP.get(prediction, 0)

    if disease == "Cataract":
        return CATARACT_CLASS_MAP.get(prediction, 0)

    return 0


def build_clinical_report(disease, prediction, confidence, keywords):

    if disease == "Glaucoma":
        confidence = 1 - confidence

    if disease == "Cataract":
        confidence = 1 - confidence

    config = DISEASE_CONFIG[disease]

    class_id = get_class_id(disease, prediction)

    class_name = config["class_names"][class_id]

    template = config["templates"][class_id]

    risk = config["risk_info"][class_id]["level"]

    advice = config["clinical"][class_id]

    kw = ", ".join(keywords) if keywords else "retinal abnormalities"

    explanation = template.format(
        conf=confidence,
        kw=kw,
        zones="key retinal regions"
    )

    return {
        "disease": disease,
        "stage": class_name,
        "risk": risk,
        "explanation": explanation,
        "advice": advice
    }