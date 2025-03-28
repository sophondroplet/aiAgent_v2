from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any

import logfire
from httpx import AsyncClient

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter
)

from typing import Annotated, List

logfire.configure(send_to_logfire=os.environ.get('LOGFIRE_TOKEN'))


client = OpenAIModel(
    model_name='google/gemini-2.0-flash-lite-preview-02-05:free',
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

chatbot_agent = Agent(
    model = client, 
    system_prompt = (
        'be funny'),
    )

async def main():
    
    chat_history : Annotated[List[bytes], lambda x, y: x + y] =  []
    message_history: list[ModelMessage] = []

    while True:
        for message_row in chat_history:
            message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))
        
        
        user_input = input("You: ")
    
        async with chatbot_agent.run_stream(user_input, message_history = message_history) as result:
            async for text in result.stream_text():
                print(text)

        chat_history.append(result.new_messages_json())

if __name__ == "__main__":
    asyncio.run(main())