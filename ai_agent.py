"""
Enhanced SwasthAI Medical Assistant with Advanced Tool Calling
Powered by LangChain, LangGraph, and Gemini with function calling
"""
from typing import List, Dict, TypedDict, Annotated, Sequence, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from config import settings
import operator
import requests
import json


# ==================== MEDICAL TOOLS ====================

@tool
def search_medical_info(query: str) -> str:
    """
    Search for current medical information, drug interactions, treatment guidelines, 
    and latest health research from the web.
    
    Args:
        query: Medical topic, symptom, drug name, or health condition to search for
    
    Returns:
        Relevant medical information from reliable sources
    """
    try:
        from duckduckgo_search import DDGS
        
        # Use DDGS directly for better reliability
        with DDGS() as ddgs:
            results = ddgs.text(f"medical health {query}", max_results=3)
            if results:
                formatted_results = []
                for i, result in enumerate(results[:3], 1):
                    formatted_results.append(f"{i}. {result.get('title', 'N/A')}\n   {result.get('body', 'N/A')}")
                return f"Medical Information Search Results:\n\n" + "\n\n".join(formatted_results)
            else:
                return f"No search results found for '{query}'. I'll provide information from my medical knowledge base."
    except ImportError:
        return f"Search functionality temporarily unavailable. I'll provide information about {query} from my medical knowledge base."
    except Exception as e:
        return f"Search temporarily unavailable: {str(e)}. I'll provide information about {query} from my medical knowledge base."


@tool
def search_wikipedia_medical(query: str) -> str:
    """
    Search Wikipedia for detailed information about diseases, medical conditions,
    anatomy, medical procedures, and health topics.
    
    Args:
        query: Medical condition, disease, body part, or health topic
    
    Returns:
        Detailed encyclopedic information from Wikipedia
    """
    try:
        wikipedia = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=3000,
                lang="en"
            )
        )
        result = wikipedia.run(query)
        if not result or "Page" in result and "does not exist" in result:
            return f"Wikipedia information not available for '{query}'. The page may not exist or there may be a connection issue."
        return f"Wikipedia Medical Info:\n{result}"
    except Exception as e:
        error_msg = str(e)
        return f"Unable to access Wikipedia at the moment: {error_msg}. This could be due to network issues or Wikipedia API limitations. I can still provide general medical information about {query} from my training data."


@tool
def check_drug_interactions(drug_name: str) -> str:
    """
    Check for drug interactions, side effects, and basic medication information.
    Use this when patients mention taking medications or ask about medicines.
    
    Args:
        drug_name: Name of the medication
    
    Returns:
        Information about the drug including common side effects and precautions
    """
    try:
        # Using OpenFDA API for drug information
        url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}&limit=1"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                result = data['results'][0]
                info = {
                    'drug_name': drug_name,
                    'warnings': result.get('warnings', ['No warnings available'])[0][:500] if result.get('warnings') else 'N/A',
                    'indications': result.get('indications_and_usage', ['No information available'])[0][:500] if result.get('indications_and_usage') else 'N/A',
                }
                return json.dumps(info, indent=2)
        
        # Fallback to web search
        search = DuckDuckGoSearchRun()
        return search.run(f"{drug_name} medication side effects interactions")
    except Exception as e:
        return f"Unable to retrieve drug information for {drug_name}. Please consult a pharmacist."


@tool
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """
    Calculate Body Mass Index (BMI) and provide health category.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        BMI value and health category interpretation
    """
    try:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
            advice = "Consider consulting a nutritionist for healthy weight gain."
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            advice = "Great! Maintain your healthy lifestyle."
        elif 25 <= bmi < 30:
            category = "Overweight"
            advice = "Consider regular exercise and balanced diet."
        else:
            category = "Obese"
            advice = "Please consult a doctor for personalized health plan."
        
        return f"""BMI Calculation Results:
- BMI: {bmi:.1f}
- Category: {category}
- Recommendation: {advice}

Note: BMI is a general indicator and doesn't account for muscle mass, age, or other factors."""
    except Exception as e:
        return f"Error calculating BMI: {str(e)}"


@tool
def get_emergency_guidance(symptom: str) -> str:
    """
    Provide immediate guidance for emergency symptoms and when to seek urgent care.
    Use this for serious symptoms like chest pain, severe bleeding, breathing problems.
    
    Args:
        symptom: The emergency symptom being experienced
    
    Returns:
        Emergency guidance and whether immediate medical attention is needed
    """
    emergency_keywords = {
        'chest pain': '🚨 EMERGENCY: Call ambulance immediately (102/108). This could be a heart attack.',
        'breathing': '🚨 EMERGENCY: Seek immediate medical help. Difficulty breathing requires urgent care.',
        'severe bleeding': '🚨 EMERGENCY: Apply pressure to wound and call for emergency help immediately.',
        'stroke': '🚨 EMERGENCY: Call 102/108 immediately. Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call.',
        'snake bite': '🚨 EMERGENCY: Keep calm, immobilize affected area, go to nearest hospital immediately.',
        'poisoning': '🚨 EMERGENCY: Call poison control or go to emergency room immediately.',
        'severe burn': '🚨 EMERGENCY: Cool with water, cover with clean cloth, seek immediate medical care.',
        'unconscious': '🚨 EMERGENCY: Call 102/108, check breathing, put in recovery position if breathing.',
    }
    
    symptom_lower = symptom.lower()
    for keyword, guidance in emergency_keywords.items():
        if keyword in symptom_lower:
            return f"{guidance}\n\nEmergency Numbers India:\n- Ambulance: 102 or 108\n- Emergency: 112"
    
    return """Based on symptoms, if any of these apply, seek immediate care:
- Severe pain (chest, abdomen, head)
- Difficulty breathing
- Heavy bleeding
- Loss of consciousness
- High fever with confusion
- Severe allergic reaction

Call 102, 108, or 112 for emergency services in India."""


@tool
def search_nearby_facilities(location: str, facility_type: str = "hospital") -> str:
    """
    Help find nearby healthcare facilities like hospitals, clinics, or pharmacies.
    
    Args:
        location: City, district, or area name
        facility_type: Type of facility (hospital, clinic, pharmacy, diagnostic_center)
    
    Returns:
        Information about how to find nearby healthcare facilities
    """
    return f"""To find {facility_type}s near {location}:

1. Google Maps: Search "{facility_type} near {location}"
2. Call 108 (Ambulance) - they can direct you to nearest facility
3. Use Practo or 1mg app for hospitals/clinics/pharmacies
4. Government Health Helpline: 104 (medical advice)

For Primary Health Centers (PHC):
- Visit your local PHC for free/subsidized care
- Ask your village Sarpanch for nearest PHC location

For emergencies, call 102 or 108 immediately."""


@tool
def general_health_tips(topic: str) -> str:
    """
    Provide evidence-based health tips on nutrition, exercise, hygiene, 
    preventive care, and healthy lifestyle habits.
    
    Args:
        topic: Health topic like nutrition, exercise, hygiene, mental health, etc.
    
    Returns:
        Practical health tips and recommendations
    """
    tips_database = {
        'nutrition': """Healthy Eating Tips:
- Eat variety: Include grains, pulses, vegetables, fruits
- Traditional Indian diet (dal-roti-sabzi) is well-balanced
- Drink 8-10 glasses of water daily
- Limit sugar, salt, and fried foods
- Include seasonal fruits and vegetables
- Don't skip breakfast""",
        
        'exercise': """Physical Activity Guidelines:
- 30 minutes of activity daily (walking, yoga, cycling)
- Traditional exercises: Surya Namaskar, yoga asanas
- Farming and household work also count as exercise
- Start slowly and gradually increase
- Stay hydrated during activity""",
        
        'hygiene': """Hygiene Best Practices:
- Wash hands with soap before eating and after toilet
- Drink clean, boiled/filtered water
- Keep surroundings clean to prevent mosquitoes
- Take regular baths
- Trim nails regularly
- Cover mouth when coughing/sneezing""",
        
        'mental health': """Mental Wellness Tips:
- Talk to trusted friends/family about feelings
- Practice deep breathing or meditation
- Maintain regular sleep schedule
- Stay connected with community
- Seek help if feeling very sad/anxious
- Helpline: KIRAN 1800-599-0019 (mental health)"""
    }
    
    topic_lower = topic.lower()
    for key, tips in tips_database.items():
        if key in topic_lower:
            return tips
    
    return "For specific health tips, please mention: nutrition, exercise, hygiene, or mental health."


# ==================== SYSTEM PROMPT ====================

ENHANCED_MEDICAL_PROMPT = """You are SwasthAI, an advanced AI medical assistant specifically designed for rural healthcare in India. You have access to multiple tools to provide accurate, up-to-date medical information.

YOUR TOOLS & WHEN TO USE THEM:
1. search_medical_info: For current medical information, treatments, latest research
2. search_wikipedia_medical: For detailed disease/condition information
3. check_drug_interactions: When patients mention medications
4. calculate_bmi: When weight and height are provided
5. get_emergency_guidance: For ANY potentially serious symptoms
6. search_nearby_facilities: When patients need to find healthcare facilities
7. general_health_tips: For preventive care and healthy lifestyle advice

IMPORTANT INSTRUCTIONS:
- ALWAYS use get_emergency_guidance first if symptoms sound serious
- Use search_medical_info for recent health information
- Try Wikipedia for comprehensive background information
- **If tools fail or return errors, CONFIDENTLY use your extensive medical training data**
- **DO NOT apologize repeatedly - simply provide the medical information directly**
- You have been trained on vast medical knowledge - use it when tools are unavailable
- Mention tool limitations once briefly, then continue with comprehensive information
- Be proactive in using tools when available
- When multiple tools are relevant, use them to provide comprehensive answers
- After using tools, synthesize the information in simple, empathetic language

YOUR APPROACH:
1. Listen carefully and identify if emergency guidance is needed
2. Use appropriate tools to gather information
3. Combine tool results with your medical knowledge
4. Explain in simple Hindi-English mix (Hinglish) when helpful
5. Always be empathetic and culturally sensitive
6. Clarify that you provide guidance, not diagnosis

RED FLAGS (Use get_emergency_guidance immediately):
- Chest pain, breathing difficulty
- Severe bleeding, injuries
- Snake bites, poisoning
- High fever with confusion
- Stroke symptoms
- Severe abdominal pain
- Pregnancy complications

Communication Style:
- Warm and friendly, like a trusted healthcare worker
- Break complex information into simple steps
- Use examples rural communities understand
- Show empathy and acknowledge concerns
- Encourage seeking professional care when needed

Remember: You're an intelligent assistant with access to current information. Use your tools wisely to provide the best possible guidance while being clear about limitations."""


# ==================== AGENT STATE ====================

class AgentState(TypedDict):
    """Enhanced state with tool support"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_history: List[Dict[str, str]]


# ==================== SWASTHAI AGENT ====================

class EnhancedSwasthAIAgent:
    """
    Enhanced SwasthAI Medical Assistant with Tool Calling
    Uses Gemini 2.5 Flash with function calling for intelligent responses
    """
    
    def __init__(self):
        """Initialize the enhanced AI agent"""
        self.tools = self._initialize_tools()
        self.llm = self._initialize_llm()
        self.graph = self._build_graph()
    
    def _initialize_tools(self):
        """Initialize all available tools"""
        return [
            search_medical_info,
            search_wikipedia_medical,
            check_drug_interactions,
            calculate_bmi,
            get_emergency_guidance,
            search_nearby_facilities,
            general_health_tips,
        ]
    
    def _initialize_llm(self):
        """Initialize Gemini with function calling"""
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in environment")
        
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7,
                max_output_tokens=2000,
                convert_system_message_to_human=True
            )
            # Bind tools to the LLM
            return llm.bind_tools(self.tools)
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini: {e}")
    
    def _build_graph(self) -> StateGraph:
        """Build the conversation flow graph with tool support"""
        
        def should_continue(state: AgentState) -> str:
            """Determine if tools should be called"""
            messages = state["messages"]
            last_message = messages[-1]
            
            # If the LLM makes a tool call, route to tools
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            # Otherwise, end
            return "end"
        
        def call_model(state: AgentState) -> AgentState:
            """Call the LLM with tool support"""
            messages = state["messages"]
            
            # Add system prompt
            full_messages = [SystemMessage(content=ENHANCED_MEDICAL_PROMPT)] + list(messages)
            
            # Get response from LLM (may include tool calls)
            response = self.llm.invoke(full_messages)
            
            return {
                "messages": [response],
                "conversation_history": state.get("conversation_history", [])
            }
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "end": END
            }
        )
        
        # Tools always go back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile the graph
        return workflow.compile()
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Process user message with tool support
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation context
        
        Returns:
            AI assistant's response (may include tool results)
        """
        # Convert conversation history
        messages = []
        if conversation_history:
            for msg in conversation_history[-10:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=user_message))
        
        # Run the graph
        state = {
            "messages": messages,
            "conversation_history": conversation_history or []
        }
        
        result = self.graph.invoke(state)
        
        # Extract final AI response
        for message in reversed(result["messages"]):
            if isinstance(message, AIMessage) and message.content:
                return message.content
        
        return "I apologize, I couldn't process that. Could you please rephrase?"
    
    def get_greeting(self) -> str:
        """Get enhanced greeting message"""
        return """Namaste! 🙏 I'm SwasthAI, your intelligent AI medical assistant.

I now have access to:
✅ Current medical research and information
✅ Detailed disease and condition database (Wikipedia)
✅ Drug interaction checker
✅ BMI calculator
✅ Emergency guidance system
✅ Healthcare facility locator
✅ Evidence-based health tips

I can help you with:
- Understanding symptoms and conditions
- Checking medication information
- Emergency guidance
- Finding nearby healthcare
- General health advice
- When to see a doctor

How can I assist you today? 🏥"""


# Global enhanced agent instance
_enhanced_agent = None


def get_enhanced_agent() -> EnhancedSwasthAIAgent:
    """Get or create the global enhanced agent"""
    global _enhanced_agent
    if _enhanced_agent is None:
        _enhanced_agent = EnhancedSwasthAIAgent()
    return _enhanced_agent


# Backward compatibility alias
def get_agent() -> EnhancedSwasthAIAgent:
    """Get or create the global agent (backward compatibility)"""
    return get_enhanced_agent()


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Initializing Enhanced SwasthAI Agent...")
    agent = EnhancedSwasthAIAgent()
    print("✅ Agent initialized successfully!\n")
    print(agent.get_greeting())
    
    # Test conversations
    test_queries = [
        "I have chest pain and difficulty breathing",
        "What are the symptoms of dengue fever?",
        "Can you calculate my BMI? I weigh 70 kg and my height is 175 cm",
        "I'm taking aspirin daily. What should I know about it?",
    ]
    
    print("\n" + "="*60)
    print("TESTING ENHANCED AGENT WITH TOOL CALLING")
    print("="*60 + "\n")
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        print(f"🤖 SwasthAI: ", end="", flush=True)
        response = agent.chat(query)
        print(response)
        print("-" * 60)