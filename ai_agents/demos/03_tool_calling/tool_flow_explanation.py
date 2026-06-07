import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
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

# Define a simple tool
def get_weather(city: str) -> str:
    """Get weather information for a city"""
    # Simulate weather data
    weather_data = {
        "london": "Sunny, 22°C",
        "paris": "Cloudy, 18°C",
        "tokyo": "Rainy, 15°C",
        "new york": "Windy, 12°C"
    }
    return weather_data.get(city.lower(), "Weather data not available")

# Create model with tools
tools = [get_weather]
model_with_tools = model.bind_tools(tools)

def tool_calling_llm(state: MessagesState):
    """LLM node that can call tools"""
    print("🤖 LLM Processing: Analyzing user request...")
    return {"messages": model_with_tools.invoke(state["messages"])}

def create_flow_demo_agent():
    """Create agent to demonstrate the flow"""
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
    print("🔄 Tool Agent Flow Explanation")
    print("=" * 50)
    
    # Create the agent
    agent = create_flow_demo_agent()
    
    print("Flow Steps:")
    print("1. User asks a question")
    print("2. Agent analyzes the question")
    print("3. Agent decides if tools are needed")
    print("4. If yes: Agent calls the tool")
    print("5. Tool executes and returns result")
    print("6. Agent provides final answer")
    print()
    
    # Test with a question that needs a tool
    print("--- Example: Weather Question ---")
    messages = [HumanMessage(content="What's the weather like in Delhi?")]
    result = agent.invoke({"messages": messages})
    
    print("\nConversation Flow:")
    for i, msg in enumerate(result["messages"], 1):
        if isinstance(msg, HumanMessage):
            print(f"{i}. Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"{i}. AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   → Tool Call: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})")
        else:
            print(f"{i}. Tool Result: {msg.content}")
    
    print("\n--- Example: Non-Tool Question ---")
    messages = [HumanMessage(content="Hello, how are you?")]
    result = agent.invoke({"messages": messages})
    
    print("\nConversation Flow:")
    for i, msg in enumerate(result["messages"], 1):
        if isinstance(msg, HumanMessage):
            print(f"{i}. Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"{i}. AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   → Tool Call: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})")
        else:
            print(f"{i}. Tool Result: {msg.content}")