"""
File: classifier.py

Purpose: Loads the trained classification model and predicts the category of customer messages.

"""

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import joblib

# ---------------------------------------------------------
# Load the trained model.
# This happens once when the module is imported.
# ---------------------------------------------------------

model = joblib.load("models/conversation_classifier.pkl")

# ---------------------------------------------------------
# Predict the category of a customer message
# ---------------------------------------------------------

"""
Function to predict the business category of a customer message.

Parameters - message (str) - The customer's message.

Returns - str - The predicted conversation category.

"""

def predict_category(message):
    prediction = model.predict([message])
    return prediction[0]


