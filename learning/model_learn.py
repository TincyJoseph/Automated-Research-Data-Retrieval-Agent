"""Model provides reasoning for the agent,determining which tools to call, how to interpret results, and when to provide a final answer.
   Usually a model can do text generation,but some can have tool calling capabilities,multi-step reasoning
   can provide structured output and some can give output other than text.

  Model can be specified inside the agent
     #OR
  Outside agent loop as stand alone"""

#stand alone model

import os
from langchain.chat_models import init_chat_model
os.environ["OPENAI-API-KEY"]=""
model=init_chat_model("gpt-4.1")
#--------------------1. invocation using invoke method----------------------------------------------------
#a.Single message
model.invoke("what is biasing")
#b. list of messages
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")

#or use message objects
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")

#--------------------1. invocation using stream method----------------------------------------------------
#Calling stream() returns an iterator that yields output chunks as they are produced.
full = None  # None | AIMessageChunk
for chunk in model.stream("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.text)
#--------------------1. invocation using batching method----------------------------------------------------
#Batching a collection of independent request to a model allows processing the requests in parallel
responses = model.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)

#to get each response as the requests are processed 

responses=model.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])

#If too many requests in batch mention max_concurrency also

response=model._batch(list_of_inputs,config={"max_concurrency":3})

#-----------------------Tool calling--------------------
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = model.bind_tools([get_weather])  

response = model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")