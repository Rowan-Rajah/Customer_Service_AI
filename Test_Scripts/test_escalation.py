from App.escalation import requires_human_review

# ---------------------------------------------------------
# Test 1 - Normal question
# ---------------------------------------------------------

result = requires_human_review("What laptops do you sell?")

print("Normal question:", result)

# ---------------------------------------------------------
# Test 2 - Customer requests a human
# ---------------------------------------------------------

result = requires_human_review("I want to speak to a human")

print("Human request:", result)

# ---------------------------------------------------------
# Test 3 - Serious complaint
# ---------------------------------------------------------

result = requires_human_review("I was charged twice for my order")

print("Serious complaint:", result)

# ---------------------------------------------------------
# Test 4 - AI cannot answer
# ---------------------------------------------------------

result = requires_human_review("Can you cancel my order?", "I'm not sure how to process that request. Please contact a human representative.")

print("AI cannot answer:", result)


