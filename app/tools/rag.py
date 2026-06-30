from app.services.rag import rag_store

def rag_tool(question: str):
    results = rag_store.search(question)
    print("===QUESTION===")
    print(question)
    print("===SEARCH RESULT===")    
    for result in results:
        print(result["score"])
    if not rag_store.is_match(results):
        return None
    
    context = rag_store.build_context(question)
    return context
        