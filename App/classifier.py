"""
File: classifier.py

Purpose:
Loads the trained classification model and predicts
the category of customer messages.
"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import joblib

from pathlib import Path


# ---------------------------------------------------------
# Model File Location
# ---------------------------------------------------------

# classifier.py is inside:
# github_temp/App/
#
# The trained model is inside:
# github_temp/models/
#
# Therefore, we go:
# App -> github_temp -> models

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "conversation_classifier.pkl"
)


# ---------------------------------------------------------
# Load the trained model
# ---------------------------------------------------------

model = joblib.load(
    MODEL_PATH
)


# ---------------------------------------------------------
# Predict the category of a customer message
# ---------------------------------------------------------

def predict_category(message):

    prediction = model.predict(
        [message]
    )

    return prediction[0]



