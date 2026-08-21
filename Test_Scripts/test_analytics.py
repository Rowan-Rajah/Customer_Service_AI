from analytics import get_dashboard_statistics
from analytics import get_database_statistics


print("Testing conversation analytics...")

dashboard = get_dashboard_statistics()

print("\nConversation statistics:")

print(
    "Total messages:",
    dashboard["total_messages"]
)

print(
    "Customer messages:",
    dashboard["customer_messages"]
)

print(
    "AI responses:",
    dashboard["assistant_messages"]
)

print(
    "Positive:",
    dashboard["positive"]
)

print(
    "Neutral:",
    dashboard["neutral"]
)

print(
    "Negative:",
    dashboard["negative"]
)

print(
    "Human review:",
    dashboard["human_review_count"]
)


print("\nTesting product database statistics...")

database = get_database_statistics()

print(
    "Products:",
    database["total_products"]
)

print(
    "Categories:",
    database["total_categories"]
)

print(
    "Stock:",
    database["total_stock"]
)

print(
    "Out of stock:",
    database["out_of_stock"]
)

