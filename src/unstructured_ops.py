from src.vector_store import load_vector_db

def retrieve_knowledge(query: str, k: int = 4) -> str:
    """
    Performs Semantic Search on the Vector Database (FAISS).
    
    Args:
        query (str): The user's natural language question (e.g., "Is it safe?").
        k (int): Number of text chunks to retrieve.
        
    Returns:
        str: A single string containing the combined content of the top k matches.
    """
    print(f" Searching Knowledge Base for: '{query}'")
    
    #Load the Brain 
    vectorstore = load_vector_db()
    
    if vectorstore is None:
        return "Error: Knowledge Base (Vector DB) not found. Please run 'build_kb.py' first."

   
    try:
        
        docs = vectorstore.similarity_search(query, k=k)
        
        if not docs:
            return "No relevant information found in documents."

   
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content.replace("\n", " ")
            context_parts.append(f"[Source {i}: {source}]\n{content}")
            
        final_context = "\n\n".join(context_parts)
        return final_context

    except Exception as e:
        print(f" Retrieval Error: {e}")
        return "Error retrieving information."


if __name__ == "__main__":
   
    test_q = "What are the safety guidelines for passengers?"
    
    print("\n RETRIEVED CONTEXT ")
    print(retrieve_knowledge(test_q))