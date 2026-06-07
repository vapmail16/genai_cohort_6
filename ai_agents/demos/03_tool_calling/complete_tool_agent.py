import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

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
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Create model with tools
tools = [add, subtract, multiply, divide]
model_with_tools = model.bind_tools(tools)

def tool_calling_llm(state: MessagesState):
    """LLM node that can call tools"""
    return {"messages": model_with_tools.invoke(state["messages"])}

def create_tool_agent():
    """Create a complete tool-calling agent"""
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", END)
    
    return builder.compile()

if __name__ == "__main__":
    print("🤖 Complete Tool Agent Demo")
    print("=" * 50)
    
    # Create the agent
    agent = create_tool_agent()
    
    # Test questions
    test_questions = [
        "What is 15 plus 25?",
        "Calculate 100 minus 37",
        "What is 8 times 9?",
        "What is 50 divided by 5?",
        "Calculate 2 plus 3, then multiply by 4"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test {i} ---")
        print(f"Question: {question}")
        print()
        
        # Process with agent
        messages = [HumanMessage(content=question)]
        result = agent.invoke({"messages": messages})
        
        # Display the conversation
        for msg in result["messages"]:
            if isinstance(msg, HumanMessage):
                print(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                print(f"AI: {msg.content}")
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"  Tool Call: {tool_call['name']}({tool_call['args']})")
            elif isinstance(msg, ToolMessage):
                print(f"Tool Result: {msg.content}")
        print()