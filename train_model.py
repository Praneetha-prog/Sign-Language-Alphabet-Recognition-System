import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import pickle

# Load dataset
data = pd.read_csv("dataset.csv")

# Split features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Shuffle FIRST
X, y = shuffle(X, y)

# Then split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=200, max_depth=20)
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")