import torch
import torchvision.models as models
from tensorflow.keras.models import load_model


def load_all_models():

    models_dict = {}

    # TensorFlow models
    models_dict["dr"] = load_model("models/dr_resnet50.h5")
    models_dict["glaucoma"] = load_model("models/glaucoma_efficientnetb0.h5")
    models_dict["cataract"] = load_model("models/cataract_efficientnetb0.h5")

    # PyTorch DME model (EfficientNet-B3)
    dme_model = models.efficientnet_b3(weights=None)

    # change classifier for 2 classes
    dme_model.classifier[1] = torch.nn.Linear(1536, 1)

    # load weights
    state_dict = torch.load("models/dme_efficientnetb3.pth", map_location="cpu")
    dme_model.load_state_dict(state_dict)

    dme_model.eval()

    models_dict["dme"] = dme_model

    return models_dict