"""
SwasthAI Medical Assistant powered by LangChain and LangGraph
This module creates an intelligent AI agent for medical consultation
"""
from typing import List, Dict, TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from config import settings
import operator


# System prompt for the medical assistant
MEDICAL_ASSISTANT_PROMPT = """You are SwasthAI, a compassionate and knowledgeable AI medical assistant designed specifically for rural healthcare in India.

Your Core Responsibilities:
1. Listen carefully to health concerns and symptoms
2. Ask relevant follow-up questions to understand the situation better
3. Provide clear, simple medical guidance in easy-to-understand language
4. Show empathy and cultural sensitivity
5. Explain medical terms whenever you use them

Important Guidelines:
- ALWAYS be supportive and non-judgmental
- Use simple Hindi-English mix (Hinglish) when helpful
- For serious symptoms, URGENTLY advise seeing a doctor
- Never provide definitive diagnoses - offer general guidance only
- Consider limited healthcare access in rural areas
- Suggest home remedies when appropriate and safe
- Be aware of common rural health issues (water-borne diseases, malnutrition, snake bites, etc.)

Communication Style:
- Friendly and warm, like talking to a trusted healthcare worker
- Break complex information into simple steps
- Use examples and analogies that rural communities understand
- Ask one question at a time
- Acknowledge feelings and concerns

Red Flags (Always recommend urgent medical attention):
- Severe chest pain or breathing difficulty
- High fever with stiff neck or confusion
- Severe bleeding or injuries
- Snake bites or poisoning
- Severe abdominal pain
- Signs of stroke (facial drooping, arm weakness, speech difficulty)
- Pregnancy complications
- Severe dehydration in children

Remember: You are a supportive first point of contact, not a replacement for doctors. Your goal is to educate, guide, and help people make informed healthcare decisions."""


class AgentState(TypedDict):
    """State of the conversation agent"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_history: List[Dict[str, str]]


class SwasthAIAgent:
    """
    SwasthAI Medical Assistant Agent using LangGraph
    Provides intelligent, context-aware medical guidance
    """
    
    def __init__(self):
        """Initialize the AI agent with selected provider"""
        self.llm = self._initialize_llm()
        self.graph = self._build_graph()
    
    def _initialize_llm(self):
        """Initialize the language model based on configuration"""
        if settings.AI_PROVIDER == "gemini":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not set in environment")
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7,
                max_output_tokens=500
            )
        else:  # default to OpenAI
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment")
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=500,
                openai_api_key=settings.OPENAI_API_KEY
            )
    
    def _build_graph(self) -> StateGraph:
        """Build the conversation flow graph using LangGraph"""
        
        # Define the agent node
        def agent_node(state: AgentState) -> AgentState:
            """Process user message and generate response"""
            messages = state["messages"]
            
            # Add system prompt at the beginning
            full_messages = [SystemMessage(content=MEDICAL_ASSISTANT_PROMPT)] + list(messages)
            
            # Get response from LLM
            response = self.llm.invoke(full_messages)
            
            return {
                "messages": [response],
                "conversation_history": state.get("conversation_history", [])
            }
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", agent_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add edge to end
        workflow.add_edge("agent", END)
        
        # Compile the graph
        return workflow.compile()
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Process a user message and return AI response
        
        Args:
            user_message: The user's message
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI assistant's response
        """
        # Convert conversation history to LangChain messages
        messages = []
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        # Run the graph
        state = {
            "messages": messages,
            "conversation_history": conversation_history or []
        }
        
        result = self.graph.invoke(state)
        
        # Extract AI response
        ai_message = result["messages"][-1]
        return ai_message.content
    
    def get_greeting(self) -> str:
        """Get a friendly greeting message"""
        return """Namaste! 🙏 I'm SwasthAI, your friendly AI medical assistant.

I'm here to help you with:
- Understanding your symptoms
- General health guidance
- When to see a doctor
- Basic health tips

How can I help you today? Feel free to tell me about any health concerns you have."""


# Global agent instance
_agent_instance = None


def get_agent() -> SwasthAIAgent:
    """Get or create the global agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SwasthAIAgent()
    return _agent_instance


# Test the agent
if __name__ == "__main__":
    agent = SwasthAIAgent()
    print("SwasthAI Agent initialized successfully!")
    print("\n" + agent.get_greeting())
    
    # Test conversation
    response = agent.chat("I have a headache and mild fever since yesterday")
    print(f"\nAI: {response}")
