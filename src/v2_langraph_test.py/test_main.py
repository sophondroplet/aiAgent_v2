from __future__ import annotations
import asyncio
from langgraph.types import Command
from graph import agentic_flow

async def stream_message(flag, user_input: str = "Hello"): 
    config = {"configurable": {"thread_id": "1"}}

    if flag:
        print("first run route")
        async for event in agentic_flow.astream(
                {"message_latest": user_input}, config, stream_mode="values"
        ):
            yield event
    
    else:
        print("second run route")
        async for event in agentic_flow.astream(
            Command(resume=user_input),
            config,
            stream_mode="values",
        ):
            
            yield event

async def main():
    is_first_chunk = True
    while True:
        
        user_input = input('you: ')

        async for chunk in stream_message(is_first_chunk, user_input):
            print(chunk)
         
        is_first_chunk = False

    
if __name__ == "__main__":
    asyncio.run(main())
