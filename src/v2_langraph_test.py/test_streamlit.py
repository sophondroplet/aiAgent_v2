import streamlit as st
import asyncio
from list import Mylist 


def stream_message(user_input: str = "Hello"): 

    mylist = Mylist
    
    for event in mylist:
            yield event


async def main():

    st.title("Prototype chatbot")
    st.write("Chat with me!")
        
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
            for chunk in stream_message(user_input):
                response_content += chunk
                # Update the placeholder with the current response content
                message_placeholder.markdown(response_content)
            
        st.session_state.messages.append({"type": "ai", "content": response_content})

if __name__ == "__main__":
    asyncio.run(main())