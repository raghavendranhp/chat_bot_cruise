import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.models import CruiseSearchQuery


load_dotenv()

def load_prompt():
    """Reads the extractor prompt from the config folder."""
    prompt_path = os.path.join("config", "extractor_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(" Warning: config/extractor_prompt.txt not found.")
        return ""

def get_extraction_chain():
    """
    Creates the LLM Chain that converts: 
    User Text -> JSON Object (CruiseSearchQuery)
    """
    
    #setup he bain 
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
    )

    #Setup the Parser 
    parser = PydanticOutputParser(pydantic_object=CruiseSearchQuery)

    #setup the rompt
    system_instruction = load_prompt()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_instruction}\n\n{format_instructions}"),
        ("human", "{query}"),
    ])

    #connect everything
    chain = prompt | llm | parser
    return chain

def extract_intent(user_query: str):
    """
    Main function to call from your Orchestrator.
    Returns: CruiseSearchQuery object (Intent + Filters)
    """
    chain = get_extraction_chain()
    parser = PydanticOutputParser(pydantic_object=CruiseSearchQuery)
    
    try:
        print(f"Extracting intent from: '{user_query}'")
        result = chain.invoke({
            "system_instruction": load_prompt(),
            "format_instructions": parser.get_format_instructions(),
            "query": user_query
        })
        return result
    except Exception as e:
        print(f" Extraction Error: {e}")
        return CruiseSearchQuery(intent="information")


if __name__ == "__main__":
    test_query = "I want a luxury Nile cruise for 5 days under $2000"
    data = extract_intent(test_query)
    print("\n EXTRACTED JSON ")
    print(data.model_dump_json(indent=2))