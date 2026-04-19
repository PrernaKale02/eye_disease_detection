import torch

from gradcam import make_gradcam_heatmap, gradcam_torch, overlay_heatmap
from preprocessing import preprocess_resnet, preprocess_efficientnet
from feature_extraction import extract_keywords_from_heatmap

def generate_explanations(image_path, models, detected):

    explanations = {}

    # DR
    if "Diabetic Retinopathy" in detected:

        img = preprocess_resnet(image_path)

        heatmap = make_gradcam_heatmap(
            img,
            models["dr"],
            "conv5_block3_out"
        )

        keywords = extract_keywords_from_heatmap(heatmap, "Diabetic Retinopathy")

        explanations["Diabetic Retinopathy"] = {
            "image": overlay_heatmap(image_path, heatmap),
            "keywords": keywords
        }

    # Glaucoma
    if "Glaucoma" in detected:

        img = preprocess_efficientnet(image_path)

        heatmap = make_gradcam_heatmap(
            img,
            models["glaucoma"],
            "top_conv"
        )

        keywords = extract_keywords_from_heatmap(heatmap, "Glaucoma")

        explanations["Glaucoma"] = {
            "image": overlay_heatmap(image_path, heatmap),
            "keywords": keywords
        }

    # Cataract
    if "Cataract" in detected:

        img = preprocess_efficientnet(image_path)

        heatmap = make_gradcam_heatmap(
            img,
            models["cataract"],
            "top_conv"
        )

        keywords = extract_keywords_from_heatmap(heatmap, "Cataract")

        explanations["Cataract"] = {
            "image": overlay_heatmap(image_path, heatmap),
            "keywords": keywords
        }

    # DME (PyTorch)
    if "Diabetic Macular Edema" in detected:

        img = preprocess_resnet(image_path)

        tensor = torch.tensor(img).permute(0,3,1,2).float()

        heatmap = gradcam_torch(models["dme"], tensor)

        keywords = extract_keywords_from_heatmap(heatmap, "Diabetic Macular Edema")

        explanations["Diabetic Macular Edema"] = {
            "image": overlay_heatmap(image_path, heatmap),
            "keywords": keywords
        }

    return explanations