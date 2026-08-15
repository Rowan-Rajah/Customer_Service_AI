"""
File: train_model.py

Purpose: Trains the conversation classification model and saves it for later use by the AI platform.

"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

# ---------------------------------------------------------
# Load the training data
# ---------------------------------------------------------

df = pd.read_csv("training/conversation_training_data.csv")


# ---------------------------------------------------------
# Features (customer messages)
# ---------------------------------------------------------

X = df["message"]

# ---------------------------------------------------------
# Labels (conversation category)
# ---------------------------------------------------------

y = df["category"]

# ---------------------------------------------------------
# Create the Machine Learning Pipeline
# ---------------------------------------------------------

model = Pipeline(
    [
        (
            "vectorizer",
            TfidfVectorizer()
        ),

        (
            "classifier",
            MultinomialNB()
        )
    ]
)

# ---------------------------------------------------------
# Train the model
# ---------------------------------------------------------

model.fit(X, y)

# ---------------------------------------------------------
# Save the trained model
# ---------------------------------------------------------

joblib.dump(
    model,
    "models/conversation_classifier.pkl"
)
print("Model trained successfully.")



