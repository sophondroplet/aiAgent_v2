import asyncio
import os
from dataclasses import dataclass
from typing import TypedDict, Annotated, List

import logfire
from httpx import AsyncClient

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, StreamWriter, interrupt

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter
)

from typing import Annotated, List

# Suppress LogfireNotConfiguredWarning
logfire.configure(send_to_logfire="never")

client = OpenAIModel(
    model_name='google/gemini-2.0-flash-lite-preview-02-05:free',
    base_url='https://openrouter.ai/api/v1',
    api_key=os.getenv('OPENROUTER_API_KEY'),
)

chatbot_agent = Agent(
    model = client, 
    system_prompt = (
        'you are a helpful assistant'),
    )

#state 
    
class AgentState(TypedDict):
    message_history:Annotated[List[bytes], lambda x, y: x + y] =  []
    message_latest:str 


async def init_test(state:AgentState):
     print("inital run!")

async def LLM_response(state:AgentState, writer: StreamWriter):

    message_history: list[ModelMessage] = []

    for message_row in state['message_history']:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))

    async with chatbot_agent.run_stream(state['message_latest'], message_history = message_history) as result:
        async for text in result.stream_text():
            writer(text)

    return {'message_history':[result.new_messages_json()]}

async def user_input(state:AgentState):
    print("interrupt start")
    human_response = interrupt({})
    print("interrupt over")
    return {'message_latest':human_response}

async def check_end(state:AgentState):
     if state['message_latest'] == '/q':
         return 'exit'
     else:
         return 'continue'

builder = StateGraph(AgentState)

# Add nodes
builder.add_node('init_test', init_test)
builder.add_node('LLM_response', LLM_response)
builder.add_node('user_input', user_input)

# Set edges
# builder.add_edge(START,'LLM_response')
builder.add_edge(START,'init_test')
builder.add_edge('init_test','LLM_response')
builder.add_edge('LLM_response','user_input')
builder.add_conditional_edges('user_input', check_end, {'exit':END, 'continue':'LLM_response'})

memory = MemorySaver()
agentic_flow = builder.compile(checkpointer = memory)
