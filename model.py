import pickle
import numpy as np

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_sign(landmarks):
    try:
        data = np.array(landmarks).reshape(1, -1)
        prediction = model.predict(data)
        return prediction[0]
    except:
        return "Unknown"