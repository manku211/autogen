
import autogen
from dotenv import load_dotenv
# from autogenvpc import gpt4_config
from config import gpt4_config 
from helpers.system_message import user_agent_task, create_vpc,create_redis,create_user
from autogen.oai.openai_utils import config_list_from_dotenv
from aws.createvpc import CreateVpc
from aws.createredis import CreateRedis
from aws.create_user import CreateUser

# import matplotlib.pyplot as plt
# import networkx as nx

graph_dict = {}




user_proxy = autogen.UserProxyAgent(
    name="User",
    system_message=user_agent_task,
    max_consecutive_auto_reply=10,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
    llm_config=gpt4_config,
    description="""
        You are working as a user proxy and deciding what agent should be selected according to user's input
    """,
)

create_vpc_agent = autogen.ConversableAgent(
    "create_vpc_agent",
    system_message=create_vpc,
    llm_config=gpt4_config,
    human_input_mode="NEVER"
)
create_redis_agent= autogen.ConversableAgent(
    "create_redis_agent",
    system_message=create_redis,
    llm_config=gpt4_config,
    human_input_mode="NEVER"
)
create_user_agent= autogen.ConversableAgent(
    "create_user_agent",
    system_message=create_user,
    llm_config=gpt4_config,
    human_input_mode="NEVER"
)


graph_dict[user_proxy] = [
    create_vpc_agent
]

graph_dict[create_vpc_agent] = [
    user_proxy
]
graph_dict[user_proxy] = [
   create_redis_agent 
]
graph_dict[create_redis_agent] = [
    user_proxy
]
graph_dict[user_proxy] = [
   create_user_agent 
]
graph_dict[create_user_agent] = [
    user_proxy
]



agents = [ 
    user_proxy,
    create_vpc_agent,
    create_redis_agent,
    create_user_agent
]
create_vpc=CreateVpc()
create_redis=CreateRedis()
create_user=CreateUser()


    
create_vpc_agent.register_function(
    function_map={
        'create_vpc': create_vpc.create_vpc
    }
)

create_redis_agent.register_function(
    function_map={
        'create_redis': create_redis.deploy_redis_using_docker
    }
)
user_proxy.register_function(
    function_map={
        'create_redis': create_redis.deploy_redis_using_docker
    }
)
user_proxy.register_function(
    function_map={
        'create_user': create_user.create_user
    }
)





