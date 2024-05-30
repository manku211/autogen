import os
from dotenv import load_dotenv
load_dotenv(".env")

config_list = [
    {
        "model": "gpt-4-0125-preview",
        "api_key": os.environ["OPENAI_API_KEY"],
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
            "description": "call the function and print",
            "parameters": {
                "type": "object",
                "properties": {},
                 "required": ["VPC_CIDR","VPC_NAME"]
            }
        },
        {
            "name": "create_redis",
            "description": "call the function and print",
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
                "redispassword": {
                    "type": "string",
                    "description": "password of redis",
                },
                },
                 "required": ["pem_file","instance_id","redispassword"]
            }
        }

    ]    
}