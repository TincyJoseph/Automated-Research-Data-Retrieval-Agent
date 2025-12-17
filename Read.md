### Langchain:-My Notes

Langchain is a python framework that provides easiest way to build AI agents and LLM based applications.We can integrate LLMS and vector stores of different vendors easily in Langchain.
It helps combine LLMs with :
- Prompt templates
- Chains
- Retrievers
- Vector Stores
- Agents

## Core components

# 1.Agent
An agent can automate task,can do reasoning,make decision and take the task to completion.It consists of an LLM for planning and reasoning, a set of tools that perform actions, and optional memory to retain context or past interaction.

# 2.Model
Model is the reasoning engine of agent.The model an agent uses can be specified in two ways.
    -Static:
       Model is specified once we create an agent and remains the same throughout the execution.
       
            OR
        
       Initialize a model instance using provided package.


    -Dynamic:Dynamic models are selected during runtime based on state and context.
     To use a dynamic model, create middleware using the @wrap_model_call decorator that modifies the model in the request


