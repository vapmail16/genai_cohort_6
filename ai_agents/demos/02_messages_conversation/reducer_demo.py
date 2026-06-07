from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import add_messages

print("🧩 Understanding the add_messages Reducer")
print("=" * 50)

# Step 1: Show the problem without add_messages
print("❌ Problem: Without add_messages, messages get replaced")
print()

# Simulate what happens without add_messages
old_messages = [
    HumanMessage(content="Hi how are you"),
    AIMessage(content="I am good, thank you")
]

new_message = [HumanMessage(content="What is the role of PRA in banking")]

# This would REPLACE the old messages (BAD!)
print("Old messages:")
for i, msg in enumerate(old_messages, 1):
    print(f"  {i}. {msg.content}")

print(f"\nNew message: {new_message[0].content}")

# Step 2: Show the solution with add_messages
print("\n✅ Solution: With add_messages, messages accumulate")
print()

# This COMBINES the old and new messages (GOOD!)
combined = add_messages(old_messages, new_message)

print("Combined messages:")
for i, msg in enumerate(combined, 1):
    print(f"  {i}. {msg.content}")

print(f"\nTotal messages: {len(combined)}")
print("The AI can see the full conversation history!")