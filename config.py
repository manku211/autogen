import os
from dotenv import load_dotenv
load_dotenv(".env")

config_list = [
    {
        "model": "gpt-4-0125-preview",
        "api_key": os.environ["OPENAI_API_KEY"],
        "base_url":os.environ["BASE_URL"]
    }
]

gpt4_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
    "functions": [
        {
            "name": "create_vpc",
            "description": "call the function and return the values from the function",
            "parameters": {
                "type": "object",
                "properties": {},
                 "required": ["VPC_CIDR","VPC_NAME"]
            }
        },
        {
            "name": "create_redis",
            "description": "call the function and return the values from the function",
            "parameters": {
                "type": "object",
                "properties": {
                    "pem_file": {
                    "type": "string",
                    "description": "path of pem_file",
                },
                "instance_id": {
                    "type": "string",
                    "description": "Id of the image ubuntu",
                },
                },
                 "required": ["pem_file","instance_id"]
            }
        },
        {
            "name": "create_user",
            "description": "call the function and return the values from the function",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {
                    "type": "string",
                    "description": " provide the username  for the aws",
                },
                "project_name": {
                    "type": "string",
                    "description": "provide the project name for providing bucket name",
                },
                },
                 "required": ["user_name","project_name"]
            }
        }

    ]    
}