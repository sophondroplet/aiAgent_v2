# orchestrator.py
import asyncio
from datetime import datetime, timedelta

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from graph import agentic_flow
from graph import LLM_call_request


class Orchestrator:
    def __init__(self):
        self.config = {"configurable": {"thread_id": "1"}}
        self.idle_threshold = 20  # 20 sec
        self.is_first_run = True
    async def monitor_threads(self):
        while True:
            state = agentic_flow.get_state(self.config)
            
            if self.needs_intervention(state):
                await self.trigger_followup(state)
            await asyncio.sleep(10)

    def needs_intervention(self, state):
        if self.is_first_run:
            self.is_first_run = False
            return True

        else:
            last_activity = datetime.fromisoformat(state.values["last_activity"])
            return (datetime.now() - last_activity) > timedelta(seconds=self.idle_threshold)

    async def trigger_followup(self, state):
        # Call secondary LLM
        
        # followup_needed = await self.analyze_convo_context(
        #     state.values["message_history"][-3:]
        # )
        
        # if followup_needed:
        if True:
            if self.is_first_run:
                print("sending command to LLM -- first run test")

            else:   
                print("triggered command to LLM -- second run test")

                await asyncio.sleep(10)

                print("sending command to LLM -- second run test")
                # async for event in agentic_flow.astream(
                #     Command(resume=
                #         {
                #         'call_reason':'LLM_thought',
                #         'call_content':'User has been inactive. Initiate follow-up conversation.'
                #         }
                #         ),
                #     self.config
                # ):
                #     print(event)

                async for event in agentic_flow.astream(
                {"user_message_latest": 'User has been inactive. Initiate follow-up conversation.'}, self.config, stream_mode="custom"
                ):
                    print(event)

    async def analyze_convo_context(self, messages):
        # Implement your secondary LLM analysis here
        # Return True/False based on conversation context
        return True




#run langraph
#run UI

#access state from langgraph
#access inputs from UI
#monitor changes to state and inputs from the UI


#when state changes, activate a timer to monitor user idle time
#when UI, activate a timer to monitor user idle time

#if timer exceeds a certain threshold, activate send request to a small LLM to check if follow up is needed

#if follow up is needed, call LLM
