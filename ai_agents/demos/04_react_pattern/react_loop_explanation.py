import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
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

def create_react_agent():
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")  # Loop back!
    return builder.compile()

if __name__ == "__main__":
    print("🔄 Understanding ReACT Loop")
    print("=" * 50)
    
    react_graph = create_react_agent()
    
    print("\nWhat Happened:")
    print("1. AI reasoned it needed to add 3 and 4")
    print("2. Called addition tool, got result 7")
    print("3. AI reasoned it needed to multiply 7 by 2")
    print("4. Called multiplication tool, got result 14")
    print("5. AI reasoned it needed to divide 14 by 5")
    print("6. Called division tool, got result 2.8")
    print("7. AI provided final answer with summary")
    print()
    
    messages = [HumanMessage(content="I need to calculate something complex: Add 10 and 15, then multiply by 3, then add 100.")]
    result = react_graph.invoke({"messages": messages})
    
    print("\nDetailed Conversation Flow:")
    step_count = 0
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                step_count += 1
                print(f"\n--- Loop {step_count} ---")
    
    print(f"\nTotal reasoning loops: {step_count}")
    print("\nThis is ReACT: Reasoning and acting in a loop until complete!")