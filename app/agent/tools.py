from langchain.tools import tool
from duckduckgo_search import DDGS
from .vectorstore import get_vectorstore

# ===================== VECTORSTORE =====================
vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})


# ===================== KNOWLEDGE BASE TOOL =====================
@tool(
    description=(
        "Search the Kerala travel knowledge base for tourist places, attractions, "
        "and hotels for a given Kerala location. "
        
    )
)
def search_knowledge_base(enquery: str) -> str:
    """
    Retrieve tourism-related information from the local vector store.
    """
    if not enquery or not enquery.strip():
        return "Invalid place name provided."

    docs = retriever.invoke(enquery.strip())

    if not docs:
        return f"No information found in the knowledge base for {enquery}."

    return "\n".join(doc.page_content for doc in docs)


# ===================== DUCKDUCKGO WEB SEARCH TOOL =====================
@tool(
    description=(
        "Search online to find how to reach a Kerala tourist place. "
        "Includes nearest airport, railway station, and road access. "
        "Input must be a specific place name."
    )
)
def web_search_how_to_reach(enquery: str) -> str:
    """
    Use DuckDuckGo to find transport information for a given place.
    """
    if not enquery or not enquery.strip():
        return "Invalid place name provided."

    query = f"How to reach {enquery} Kerala nearest airport railway station bus"

    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                body = r.get("body")
                if body:
                    results.append(body)

        if not results:
            return f"No transport information found online for {enquery}."

        # Keep it short and agent-friendly
        summary = "\n".join(f"- {r}" for r in results[:3])
        return f"How to reach {enquery}:\n{summary}"

    except Exception as e:
        return f"Error fetching travel information for {enquery}: {str(e)}"
