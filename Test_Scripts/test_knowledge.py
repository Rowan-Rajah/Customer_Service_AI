
from App.knowledge_manager import load_knowledge

knowledge = load_knowledge()

for filename, text in knowledge.items():

    print("=" * 60)
    print(filename)
    print("=" * 60)

    print(text)
    print()


