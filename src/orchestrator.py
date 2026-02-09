import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#Import our Modules
from src.extractor import extract_intent
from src.structured_ops import perform_search
from src.unstructured_ops import retrieve_knowledge

load_dotenv()

def load_synthesizer_prompt():
    """Loads the instructions for the final answer generation."""
    path = os.path.join("config", "synthesizer_prompt.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "You are a helpful assistant. Answer the user based on the context provided."

def synthesize_answer(user_query, context_data, intent):
    """
    The Final Step: Takes raw data (CSV rows or Text chunks) 
    and converts it into a natural language response.
    """
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.2)
    
    system_prompt = load_synthesizer_prompt()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User Query: {query}\n\nData/Context Found:\n{context}\n\nIntent: {intent}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": user_query, "context": context_data, "intent": intent})

def run_orchestrator(user_query):
    """
    The Main Function called by Streamlit.
    """
    print(f"\n ORCHESTRATOR STARTED: '{user_query}'")
    
   
    query_object = extract_intent(user_query)
    intent = query_object.intent
    print(f" Intent Detected: {intent}")
    
    context_data = ""
    
   
    if intent in ["recommendation", "comparison"]:
        
        print(" Routing to Structured Search (CSV)")
        context_data = perform_search(query_object)
        
    elif intent == "information":
        
        print(" Routing to Unstructured Search (RAG)")
        context_data = retrieve_knowledge(user_query)
        
    elif intent == "greeting":
        return "Hello! I am SeShat, your Egypt Cruise Assistant. How can I help you plan your trip today?"


    if not context_data or "Error" in context_data:
        return "I'm sorry, I couldn't find any information matching your request."
        
    print(" Synthesizing Final Answer...")
    final_response = synthesize_answer(user_query, context_data, intent)
    
    return final_response


if __name__ == "__main__":
    
    print(run_orchestrator("Find me a luxury Nile cruise under $1500"))