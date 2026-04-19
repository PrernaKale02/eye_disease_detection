from tensorflow.keras.models import load_model

for name in ["dr_resnet50", "glaucoma_efficientnetb0", "cataract_efficientnetb0"]:
    print(f"Converting {name}...")
    model = load_model(f"models/{name}.h5", compile=False)
    model.save(f"models/{name}_v2.h5")
    print(f"Saved {name}_v2.h5")