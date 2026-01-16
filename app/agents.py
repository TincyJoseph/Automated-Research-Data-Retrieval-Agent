from typing import List
from dataclasses import dataclass
from pydantic import BaseModel, Field
import os

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from langchain.messages import SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from langgraph.checkpoint.redis import RedisSaver

# ===================== LLM =====================
llm = ChatOllama(
    model="majx13/test",
    temperature=0.1,
    num_ctx=2048,
    num_predict=256,
)

# ===================== CONTEXT =====================
@dataclass
class AgentContext:
    user_location: str = "Kerala"
    preferred_language: str = "English"

# ===================== RESPONSE SCHEMA =====================
class PlaceInfo(BaseModel):
    name: str
    attraction: str
    how_to_reach: str

class HotelsInfo(BaseModel):
    hotels_nearby: List[str]

class TravelResponse(BaseModel):
    district: str
    places: List[PlaceInfo]
    hotels: HotelsInfo

# ===================== TOOLS =====================
ddg = DuckDuckGoSearchRun()

@tool
def places_to_visit(district: str, limit: int = 3) -> str:
    query = (
        f"Top {limit} tourist places in {district} district Kerala, "
        "main attractions and how to reach, nearest railway station, bus stand, airport"
    )
    try:
        return ddg.invoke(query)
    except Exception:
        return "Unavailable"

@tool
def find_hotels(district: str) -> str:
    query = f"Best hotels and resorts to stay in {district} district Kerala"
    try:
        return ddg.invoke(query)
    except Exception:
        return "Unavailable"

# ===================== SYSTEM PROMPT =====================
system_prompt = SystemMessage(
    content="""
You are a Kerala travel planning assistant.

Rules:
- Ask for the district if not mentioned.
- Do NOT hallucinate places or hotels.
- Use tools for factual data.
- If user asks unrelated questions, politely redirect to Kerala travel.

Response:
- Always return JSON matching TravelResponse.
- If data is missing, use "Unavailable".
"""
)

# ===================== REDIS MEMORY =====================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
checkpointer = RedisSaver.from_conn_string(REDIS_URL)

# ===================== AGENT =====================
agent = create_agent(
    model=llm,
    tools=[places_to_visit, find_hotels],
    system_prompt=system_prompt,
    response_format=ToolStrategy(TravelResponse),
    context_schema=AgentContext,
    checkpointer=checkpointer,
    debug=False,
)
