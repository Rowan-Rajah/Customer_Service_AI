from App.knowledge_manager import load_knowledge
from App.knowledge_manager import search_knowledge

knowledge = load_knowledge()

question = "How much does virus removal cost?"

result = search_knowledge(question, knowledge)

print("=" * 60)
print("Customer Question:")
print(question)
print("\n" + "=" * 60)
print("Most Relevant Knowledge:")
print(result)




