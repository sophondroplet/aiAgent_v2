#streamlit_ui.py
import asyncio
from langgraph.types import Command
import streamlit as st

from graph import agentic_flow
from orchestrator import Orchestrator

async def stream_message(user_input: str = "Hello"): 
    config = {"configurable": {"thread_id": "1"}}

    if len(st.session_state.messages) == 1:
        print("first run")
        async for event in agentic_flow.astream(
                {"user_message_latest": user_input}, config, stream_mode="custom"
        ):
            yield event
    
    else:
        print("not first run")
        async for event in agentic_flow.astream(
            Command(resume={
                'call_reason':'user_input',
                'call_content':user_input
                    }),
            config,
            stream_mode="custom",
        ):
            
            yield event

async def main():
    st.title("Prototype chatbot")
    st.write("Chat with me!")
    
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = Orchestrator()
        asyncio.create_task(st.session_state.orchestrator.monitor_threads())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        message_type = message["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message["content"])

    user_input = st.chat_input("say soemthing")

    if user_input:
        #append user input to the strealit message list state
        st.session_state.messages.append({"type": "human", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for updating the message
            # Run the async generator to fetch responses
            async for chunk in stream_message(user_input):
                new_content = chunk[len(response_content):]
                response_content += new_content
                message_placeholder.markdown(response_content + "▌")
         
        st.session_state.messages.append({"type": "ai", "content": response_content})

if __name__ == "__main__":
    asyncio.run(main())
