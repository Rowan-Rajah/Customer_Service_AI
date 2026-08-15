"""
File: escalation.py

Purpose: Determines whether a customer conversation should be flagged for human review.

The first version uses simple rules rather than another AI model. This keeps the system fast, predictable and easy to understand.

"""

# -----------------------------------------------------------------------
# Escalation Keywords
# -----------------------------------------------------------------------

ESCALATION_KEYWORDS = [

    # Direct requests for human assistance
    "speak to a human",
    "talk to a human",
    "human representative",
    "human agent",
    "real person",
    "speak to someone",
    "talk to someone",
    "connect me to a person",
    "connect me to someone",

    # Complaints and serious problems
    "make a complaint",
    "file a complaint",
    "formal complaint",
    "i want to complain",
    "very unhappy",
    "extremely unhappy",
    "terrible service",
    "poor service",

    # Billing / payment problems
    "charged twice",
    "charged me twice",
    "wrong charge",
    "incorrect charge",
    "charged incorrectly",
    "payment problem",
    "payment issue",

    # Refund problems
    "i want a refund",
    "request a refund",
    "need a refund",
    "refund my money",
    "refund problem",
    "refund issue",

    # Order problems
    "order problem",
    "order issue",
    "wrong order",
    "missing order",
    "order never arrived",
    "order hasn't arrived",
]



# ---------------------------------------------------------
# Check whether human review is required
# ---------------------------------------------------------

def requires_human_review(user_message, ai_response):

    user_message = user_message.lower()
    ai_response = ai_response.lower()

    # ---------------------------------------------------------
    # Direct escalation requests
    # ---------------------------------------------------------

    for keyword in ESCALATION_KEYWORDS:
        if keyword in user_message:
            return True

    # ---------------------------------------------------------
    # AI uncertainty / inability to help
    # ---------------------------------------------------------

    uncertainty_phrases = [
        "i cannot help with this",
        "i'm unable to help",
        "i am unable to help",
        "i don't have enough information",
        "i do not have enough information",
        "please contact a human",
        "please speak to a human",
        "contact a human representative"
    ]

    for phrase in uncertainty_phrases:
        if phrase in ai_response:
            return True


    return False









