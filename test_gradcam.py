from load_models import load_all_models
from preprocessing import preprocess_resnet
from gradcam import make_gradcam_heatmap, overlay_heatmap

import matplotlib.pyplot as plt

image_path = "sample_DR.png"

models = load_all_models()

img = preprocess_resnet(image_path)

heatmap = make_gradcam_heatmap(
    img,
    models["dr"],
    last_conv_layer_name="conv5_block3_out"
)

result = overlay_heatmap(image_path, heatmap)

plt.imshow(result)
plt.axis("off")
plt.show()