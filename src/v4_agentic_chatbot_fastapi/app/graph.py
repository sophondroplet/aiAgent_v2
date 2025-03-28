import asyncio
import os
from dataclasses import dataclass
from typing import TypedDict, Annotated, List

from datetime import datetime

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
from pydantic import BaseModel

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
    system_prompt = ('you are a helpful assistant'),
    )

#state 
    
class AgentState(TypedDict):
    message_history:Annotated[List[bytes], lambda x, y: x + y] =  []
    user_message_latest:str 
    LLM_thought_latest:str 
    last_activity: str = datetime.now()

class LLM_call_request(TypedDict):
    call_reason: str
    call_content: str

async def initialize_states(state:AgentState):
     print("initalizing states")
     
     return {'message_history':[],
             'last_activity':datetime.now(),
             'LLM_thought_latest':['The user has summoned you, say a welcome message!']}

async def LLM_call(state:AgentState, writer: StreamWriter):
    print(f'before LLM call: {state}')
    
    message_history: list[ModelMessage] = []

    for message_row in state['message_history']:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))

    async with chatbot_agent.run_stream(state['user_message_latest'], message_history = message_history) as result:
        async for text in result.stream_text():
            writer(text)

    print(f'after LLM call: {state}')

    return {'message_history':[result.new_messages_json()]}

async def wait_for_LLM_call(state:AgentState):
    trigger = interrupt({})
    
    print(f'received command from LLM: {trigger}')

    if trigger['call_reason'] == 'user_input':
        return {'user_message_latest':trigger['call_content']}
    
    elif trigger['call_reason'] == 'LLM_thought':
        return {'LLM_thought_latest':trigger['call_content']}

async def check_end(state:AgentState):
     if state['user_message_latest'] == '/q':
         return 'exit'
     else:
         return 'continue'

builder = StateGraph(AgentState)

# Add nodes
builder.add_node('initialize_states', initialize_states)
builder.add_node('LLM_call', LLM_call)
builder.add_node('wait_for_LLM_call', wait_for_LLM_call)

# Set edges
# builder.add_edge(START,'LLM_call')
builder.add_edge(START,'initialize_states')
builder.add_edge('initialize_states','LLM_call')
builder.add_edge('LLM_call','wait_for_LLM_call')
builder.add_conditional_edges('wait_for_LLM_call', check_end, {'exit':END, 'continue':'LLM_call'})

memory = MemorySaver()
agentic_flow = builder.compile(checkpointer = memory)
