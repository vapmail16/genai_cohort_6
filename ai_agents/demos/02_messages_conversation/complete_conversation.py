import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages

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

def conversation_node(state: MessagesState):
    """Process conversation and return AI response"""
    print("💬 Processing conversation...")
    
    # The AI sees the full conversation history
    response = model.invoke(state["messages"])
    
    # Return the AI response
    return {"messages": [response]}

def create_conversation_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("conversation", conversation_node)
    builder.add_edge(START, "conversation")
    builder.add_edge("conversation", END)
    return builder.compile()

if __name__ == "__main__":
    print("🎯 Complete Conversation Demo")
    print("=" * 50)
    
    # Create the graph
    graph = create_conversation_graph()
    
    # Simulate a multi-turn conversation
    conversation_turns = [
        "Hi, I'm Vikkas. I work in banking.",
        "I need help understanding CRR regulations.",
        "Can you explain what CRR Article 92 means?",
        "How does this apply to TechBank International specifically?"
    ]
    
    # Start with system message
    messages = [SystemMessage(content="You are a helpful banking regulation expert.")]
    
    for i, user_input in enumerate(conversation_turns, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {user_input}")
        
        # Add user message
        messages.append(HumanMessage(content=user_input))
        
        # Process with graph
        result = graph.invoke({"messages": messages})
        
        # Get the AI response
        ai_response = result["messages"][-1]
        print(f"AI: {ai_response.content}")
        
        # Update messages for next turn
        messages = result["messages"]
    
    print(f"\n📊 Final conversation has {len(messages)} messages")
    print("The AI remembered the entire conversation context!")