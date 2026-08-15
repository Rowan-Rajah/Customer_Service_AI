"""
===========================================================
File: sentiment.py

Purpose: Analyse customer messages and determine their sentiment.

Possible results: Positive, Neutral, or Negative
===========================================================
"""

# Import TextBlob for sentiment analysis
from textblob import TextBlob

"""
Function to analyse the sentiment of a customer message.

Parameters:
message : (str) - Customer message.

Returns: (str)
Returns one of: Positive, Neutral, Negative
"""


def analyse_sentiment(message):

    # Create a TextBlob object
    blob = TextBlob(message)

    # Calculate polarity score.   
    # Range:
    # -1.0 = Very Negative
    #  0.0 = Neutral
    # +1.0 = Very Positive

    polarity = blob.sentiment.polarity

    # Determine sentiment category.

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"



