import os,time,json
import boto3
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type
import subprocess, time
import json

load_dotenv(".env")

create_amplify_json = {
    "app_name": {
                    "type": "required",
                    "description": "provide the app_name for the amplify",
                },
                "existing_repo_url": {
                    "type": "required",
                    "description": "provide the repo url for deploying",
                },
                "github_token": {
                    "type": "required",
                    "description": "provide the github token access for deploying",
                },
                "branch_name": {
                    "type": "required",
                    "description": "provide the branch name for deploying",
                },
                "enable_environment_variables":
                {
                    "type": "boolean",
                    "description": "provide provide 'TRUE' or 'FALSE' if you need env",    
                },
                # "env":
                # {
                #     "type": "required",
                #   "description": "provide provide the env if enable_environment_variables is TRUE",   
                # }
}
def write_tfvars_file(variables, file_path):
    with open(file_path, 'w') as f:
        for key, value in variables.items():
            if isinstance(value, str):
                f.write(f'{key} = "{value}"\n')
            elif isinstance(value, bool):
                f.write(f'{key} = {"true" if value else "false"}\n')
            else:
                f.write(f'{key} = {value}\n')  

# def run_remote_command(command, pem_file, instance_user_name, public_ip_address):
#         ssh_command = ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', pem_file,
#                     f"{instance_user_name}@{public_ip_address}"] + command
#         try:
#          result = subprocess.run(ssh_command, check=True, capture_output=True, text=True)
#          return result.stdout.strip()
#         except subprocess.CalledProcessError as e:
#                 print(f"An error occurred: {e}")

def run_terraform(directory):
    commands = [
        ['terraform', 'init'],
        ['terraform', 'validate'],
        ['terraform', 'plan'],
        ['terraform', 'apply', '-auto-approve']
    ]

    for command in commands:
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=directory)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running {' '.join(command)}: {e}")
            print(e.stderr)
            return False

    return True



class CreateAmplifyInput(BaseModel):
    user_name: str = Field(description="should be a string")
    project_name: str = Field(description="should be a string")

class CreateAmplify(BaseModel):
    app_name = "create_user"
    description = "create amplify  with the deployment "
    args_schema: Type[BaseModel] = CreateAmplifyInput

    region = os.getenv('REGION')
    access_key = os.getenv('ACCESS_KEY')
    secret_key = os.getenv('SECRET_KEY')

    def create_amplify(self,app_name: str,existing_repo_url: str,github_token: str, branch_name: str, enable_environment_variables: bool, env: str = ''):
      
      data = {
        'app_name':app_name,
        'existing_repo_url':existing_repo_url,
        'ssm_github_access_token_name': github_token,
        'branch_name':branch_name,
        'enable_environment_variables':enable_environment_variables,
        'aws_access_key' : self.access_key,
        'aws_secret_key' : self.secret_key,
        'region'  : self.region
        }
      file = 'terraform/amplify/terraform.tfvars'
      write_tfvars_file(data, file)
      if enable_environment_variables==True :  
        # input_env = "key1=value1\nkey2=value2\nkey3=value3"
            lines = env.strip().split('\n')
            
            # Convert each line into a key-value pair and store in a dictionary
            env_dict = {}
            for line in lines:
                key, value = line.split('=')
                env_dict[key] = value
            json_data = json.dumps(env_dict, indent=4)
            print(json_data)
        
        # Write the JSON string to a file
            with open('terraform/amplify/env.json', 'w') as json_file:
                json_file.write(json_data)
      terraform_directory = 'terraform/amplify'    
      run_terraform(terraform_directory)        
          

    