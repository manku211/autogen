import os
import autogen
from dotenv import load_dotenv
load_dotenv(".env")
from helpers.agentic import agents
from config import gpt4_config 
from helpers.agentic import user_proxy
from helpers.agentic import graph_dict
gpt4_config.pop("functions")

group_chat = autogen.GroupChat(
    agents=agents,
    messages=[],
    max_round=40,
    allow_repeat_speaker=None,
    speaker_transitions_type="allowed",
    allowed_or_disallowed_speaker_transitions=graph_dict
    
)
print(gpt4_config)
manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=gpt4_config,
    code_execution_config=False,
)

result = user_proxy.initiate_chat(
    manager,
    message="Ask from human input which agent you want to create 'VPC' or to craete 'redis'",
    clear_history=True,
)