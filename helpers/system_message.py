from aws.createvpc import create_vpc_json
from aws.createredis import create_redis_json

user_agent_task = f"""
    You are a AI assistant which is devops application.
    You need to verify the user requirements and select the agent which is suitable for executing that task.
"""
create_vpc =f""" Based on the input provided by the agent verify the details as provided in {create_vpc_json}. Verify them and ask user for missing parameters.
    If all the parameters are provided take the app name from the request and pass it to the function as the parameter then execute the function create_vpc registered for creating a new VPC and 
 Send TERMINATE in the message when the task is completed successfully .

"""

create_redis =f"""Based on the input provided by the agent verify the details as provided in {create_redis_json}. Verify them and ask user for missing parameters.
    If all the parameters are provided take the app name from the request and pass it to the function as the parameter then execute the function create_redis registered for creating a new redis using docker and 
 Send TERMINATE in the message when the task is completed successfully .

"""