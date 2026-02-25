from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_ollama import ChatOllama
from app.agent.tools import search_knowledge_base,web_search_how_to_reach
from app.agent.prompts import system_prompt
from app.agent.schemas import TravelResponse
from langchain.messages import HumanMessage
#from langgraph.prebuilt import create_agent
from langgraph.graph import StateGraph
# ===================== LLM =====================
#Using ollamachat model-this is qwen 2 model----
llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0,
    num_ctx=2048,
    num_predict=256,
)
#"majx13/test"
# ===================== AGENT =====================
tourism_agent = create_agent(
    model=llm,
    tools=[search_knowledge_base, web_search_how_to_reach],
    system_prompt=system_prompt,
    response_format=ToolStrategy(TravelResponse),
    debug=False,
)
tourism_agent.get_graph().draw_mermaid_png(output_file_path="agent_graph.png")
answer=tourism_agent.invoke({"messages": [{"role": "user", "content": "Tourist places in wayanad"}]}),
if isinstance(answer, tuple):
    answer = answer[0]

print(answer["messages"][-1].content)
