import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
tf.get_logger().setLevel("ERROR")

from predict import predict_all

def test_image(path, label):
    print("\n---------------------------")
    print(label)
    print("---------------------------")

    result = predict_all(path)

    for model in result:
        print(model, "->", result[model])



test_image("test_images/glaucoma_pos.jpg", "Glaucoma Positive")
test_image("test_images/glaucoma_neg.jpg", "Glaucoma Negative")

test_image("test_images/cataract_pos.jpg", "Cataract Positive")
test_image("test_images/cataract_neg.jpg", "Cataract Negative")

test_image("test_images/dme_pos.jpg", "DME Positive")
test_image("test_images/dme_neg.jpg", "DME Negative")

test_image("test_images/dr_pos.png", "DR Positive")
test_image("test_images/dr_neg.png", "DR Negative")