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
    "cache_seed": None,
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
        },
        {
            "name": "create_amplify",
            "description": "call the function and return the values from the function",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                    "type": "string",
                    "description": "provide the app_name for the amplify",
                },
                "existing_repo_url": {
                    "type": "string",
                    "description": "provide the repo url for deploying",
                },
                "github_token": {
                    "type": "string",
                    "description": "provide the github token access for deploying",
                },
                "branch_name": {
                    "type": "string",
                    "description": "provide the branch name for deploying",
                },
                "enable_environment_variables":
                {
                    "type": "boolean",
                    "description": "provide provide 'TRUE' or 'FALSE' if you need env",    
                },
                "env":
                {
                    "type": "string",
                  "description": "provide provide the env if enable_environment_variables is TRUE",   
                }
                },
                 "required": ["app_name","existing_repo_url","github_token","branch_name","enable_environment_variables"]
            }
        }

    ]    
}