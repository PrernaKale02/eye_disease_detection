import cv2
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input

IMG_SIZE = 224


# ------------------------------------------------
# For DR + DME models (trained with /255 scaling)
# ------------------------------------------------
def preprocess_resnet(image_path):

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

    image = image / 255.0

    image = np.expand_dims(image, axis=0)

    return image


# ------------------------------------------------
# For EfficientNet models (Glaucoma + Cataract)
# ------------------------------------------------
def preprocess_efficientnet(image_path):

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

    image = preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    return image