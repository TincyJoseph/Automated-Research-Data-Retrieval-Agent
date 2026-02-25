PROJECT: Kerala Tourism Information Agent
==================================

Overview
--------
This project implements an AI-powered tourism assistant that retrieves and generates
structured travel information about tourist destinations. The system combines:

- Vector database retrieval for knowledge grounding,uses FAISS
- LLM-based reasoning and tool usage uses Ollama model "qwen2.5:7b-instruct"
- Web search integration for additional details (e.g., how to reach) uses duckduckgo_search from langchain community
- Structured response formatting using Pydantic schemas

The agent returns organized travel information including places, attractions,
nearby hotels, and transportation guidance.


Features
--------
- Intelligent destination understanding from user queries
- Retrieval-augmented generation (RAG) using vector store
- Tool-based agent workflow
- Structured JSON output via Pydantic models
- Debug mode for workflow inspection
- Extensible architecture for adding new tools

## Project Structure

```
app/agent/
│
├── agent.py          # Agent creation and invocation
├── tools.py          # Custom tools (search_knowledge_base, web_search_how_to_reach)
├── vectorstore.py    # Vector DB initialization and retriever
├── schemas.py        # Pydantic response schemas for structured output
└── README.md         # Project documentation
```



Response Schema
---------------
The agent returns structured data in the following format:

TravelResponse
- tourist_place: str
- places: List[PlaceInfo]
- hotels: HotelsInfo
- how_to_reach: str

PlaceInfo
- name: str
- attraction: str
- how_to_reach: str

HotelsInfo
- hotels_nearby: List[str]


Sample output
--------------
{
    "tourist_place": "Wayanad",
    "places": [
        {
            "name": "Banasura Sagar Dam and nature trails",
            "attraction": "Lush forests, waterfalls, Edakkal Caves",
            "how_to_reach": "For reaching Wayanad, the nearest airport is Coimbatore (CJB) and the nearest railway station is Kalpetta. Road access is good with NH 48 and NH 212."
        }
    ],
    "hotels": {
        "Budget": ["Jungle Stay Homestay"],
        "Mid-range": ["Green Valley Resort"],
        "Premium": ["Hilltop Eco Lodge"]
    },
    "how_to_reach": "For reaching Wayanad, the nearest airport is Coimbatore (CJB) and the nearest railway station is Kalpetta. Road access is good with NH 48 and NH 212."
}

Future
---------
-Multi-Agent System for the same travel agent with agent evaluation,monitoring,docker deployment