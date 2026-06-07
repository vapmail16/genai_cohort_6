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

def division(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

tools = [addition, multiplication, division]
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
    print("🧠 Memory & Persistence Demo")
    print("=" * 50)
    
    # Create agent with memory
    agent = create_memory_agent()
    
    # Use thread_id to maintain conversation context
    config = {"configurable": {"thread_id": "demo_session_1"}}
    
    print("\n--- Turn 1: First calculation ---")
    print("User: Add 3 and 4")
    messages = [HumanMessage(content="Add 3 and 4")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Turn 2: Using context ---")
    print("User: Multiply that by 2")
    messages = [HumanMessage(content="Multiply that by 2.")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Turn 3: More context ---")
    print("User: Now divide that by 3")
    messages = [HumanMessage(content="Now divide that by 3")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n" + "=" * 50)
    print("Key Point: The agent remembered 'that' and 'that'!")
    print("Memory allows natural, contextual conversations.")
    print("=" * 50)