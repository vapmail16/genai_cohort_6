import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define tools
def addition(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

tools = [addition, multiplication]
model_with_tools = model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful arithmetic assistant.")

def assistant(state: MessagesState):
    return {"messages": model_with_tools.invoke([sys_msg] + state["messages"])}

def create_memory_agent():
    """Create agent with memory capability"""
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    # Add memory checkpointing
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("🧠 Understanding Memory Threads")
    print("=" * 50)
    
    # Create agent with memory
    agent = create_memory_agent()
    
    print("\n--- Thread 1: User Alice ---")
    config_alice = {"configurable": {"thread_id": "alice_session"}}
    
    messages = [HumanMessage(content="My favorite number is 10")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: My favorite number is 10")
    print(f"AI: {result['messages'][-1].content}")
    
    messages = [HumanMessage(content="Add 5 to my favorite number")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: Add 5 to my favorite number")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Thread 2: User Bob ---")
    config_bob = {"configurable": {"thread_id": "bob_session"}}
    
    messages = [HumanMessage(content="My favorite number is 20")]
    result = agent.invoke({"messages": messages}, config_bob)
    print(f"User Bob: My favorite number is 20")
    print(f"AI: {result['messages'][-1].content}")
    
    messages = [HumanMessage(content="Add 5 to my favorite number")]
    result = agent.invoke({"messages": messages}, config_bob)
    print(f"User Bob: Add 5 to my favorite number")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Thread 1: User Alice Continues ---")
    messages = [HumanMessage(content="What's my favorite number?")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: What's my favorite number?")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n" + "=" * 50)
    print("Key Point: Each thread maintains its own context!")
    print("Alice's favorite number is still 10, Bob's is 20.")
    print("=" * 50)