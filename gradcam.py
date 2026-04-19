import numpy as np
import cv2
import tensorflow as tf
import torch


# ------------------------------------------------
# TensorFlow Grad-CAM (DR, Glaucoma, Cataract)
# ------------------------------------------------
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        if pred_index is None:
            pred_index = tf.argmax(predictions[0])

        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    return heatmap.numpy()


# ------------------------------------------------
# PyTorch Grad-CAM (DME)
# ------------------------------------------------
def gradcam_torch(model, img_tensor):

    gradients = []
    activations = []

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    def forward_hook(module, input, output):
        activations.append(output)

    # EfficientNet last conv layer
    target_layer = model.features[-1]

    target_layer.register_forward_hook(forward_hook)
    target_layer.register_backward_hook(backward_hook)

    model.zero_grad()

    output = model(img_tensor)

    class_score = output.squeeze()

    class_score.backward()

    grads = gradients[0]
    acts = activations[0]

    weights = torch.mean(grads, dim=(2, 3), keepdim=True)

    cam = torch.sum(weights * acts, dim=1).squeeze()

    cam = torch.relu(cam)

    cam = cam / torch.max(cam)

    return cam.detach().numpy()


# ------------------------------------------------
# Overlay heatmap
# ------------------------------------------------
def overlay_heatmap(image_path, heatmap, alpha=0.4):

    img = cv2.imread(image_path)

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)

    return superimposed