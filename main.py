from predict import predict_all
from ensemble import ensemble_decision

image_path = "sample_glaucoma.jpg"

model_results = predict_all(image_path)

final_result = ensemble_decision(model_results)

print("Model outputs:")
print(model_results)

print("\nFinal diagnosis:")
print(final_result)