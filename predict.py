import torch
import numpy as np

from preprocessing import preprocess_resnet, preprocess_efficientnet
from load_models import load_all_models


# label mappings
DR_CLASSES = ["No_DR", "Mild", "Moderate", "Severe", "Proliferative_DR"]

GLAUCOMA_CLASSES = {0: "Glaucoma", 1: "Normal"}
CATARACT_CLASSES = {0: "Cataract", 1: "Normal"}

DME_CLASSES = {0: "No_DME", 1: "DME_Present"}


def predict_all(image_path):

    models = load_all_models()

    # preprocess image
    image_resnet = preprocess_resnet(image_path)
    image_effnet = preprocess_efficientnet(image_path)

    results = {}

    # ---------------- DR (TensorFlow)
    dr_pred = models["dr"].predict(image_resnet)
    dr_class = np.argmax(dr_pred)
    dr_conf = float(np.max(dr_pred))

    results["dr"] = {
        "prediction": DR_CLASSES[dr_class],
        "confidence": dr_conf
    }

    # ---------------- Glaucoma
    gl_pred = models["glaucoma"].predict(image_effnet)
    gl_prob = float(gl_pred[0][0])
    gl_class = 1 if gl_prob > 0.5 else 0

    results["glaucoma"] = {
        "prediction": GLAUCOMA_CLASSES[gl_class],
        "confidence": gl_prob
    }

    # ---------------- Cataract
    cat_pred = models["cataract"].predict(image_effnet)
    cat_prob = float(cat_pred[0][0])
    cat_class = 1 if cat_prob > 0.5 else 0

    results["cataract"] = {
        "prediction": CATARACT_CLASSES[cat_class],
        "confidence": cat_prob
    }

    # ---------------- DME (PyTorch)

    tensor = torch.tensor(image_resnet).permute(0,3,1,2).float()

    with torch.no_grad():
        dme_pred = models["dme"](tensor)
        dme_prob = torch.sigmoid(dme_pred).item()

    dme_class = 1 if dme_prob > 0.5 else 0

    results["dme"] = {
        "prediction": DME_CLASSES[dme_class],
        "confidence": dme_prob
    }

    return results