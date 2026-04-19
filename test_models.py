from load_models import load_all_models

models = load_all_models()

for name in models:
    print(name, "model loaded")