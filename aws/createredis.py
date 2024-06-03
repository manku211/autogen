import os
import boto3
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type
from typing import Annotated
import subprocess, time
import random,string

load_dotenv(".env")

create_redis_json = {
    "pemfile": {
        "description": "location of pem file",
        "type": "Required",
    },
    "instance_id": {
        "description": "instance_id to give",
        "type": "Required",
    }
}

class CreateRedisInput(BaseModel):
    pemfile: str = Field(description="should be a string")
    instance_id: str = Field(description="should be a string")

class CreateRedis(BaseModel):
    name = "create_redis"
    description = "create redis using docker"
    args_schema: Type[BaseModel] = CreateRedisInput

    region = os.getenv('REGION')
    access_key = os.getenv('ACCESS_KEY')
    secret_key = os.getenv('SECRET_KEY')
    
    def deploy_redis_using_docker(self, pem_file: str,  instance_id: str):
            instance_user_name = "ubuntu"
            password=generate_random_password()
            print(password)
            host_directory="redisdata"
            print(pem_file)

            ec2 = boto3.client(
                'ec2',
                region_name=os.getenv('REGION'),
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY')
            )

            response = ec2.describe_instances(InstanceIds=[instance_id])
            instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']


            while instance_state != 'running':
                time.sleep(30)
                response = ec2.describe_instances(InstanceIds=[instance_id])
                instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

            public_ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            

            try:
                
                create_dir_command = ['mkdir', '-p', host_directory]
                run_remote_command(create_dir_command, pem_file, instance_user_name, public_ip_address)
                docker_run_command = [
                'docker', 'run', '-d', '--name', 'my-redis',
                '--network', 'tractor',
                '-p', '6379:6379',
                '-v', f'{host_directory}:/data',
                'redis:latest', 'redis-server', '--requirepass', password
                ]
                run_remote_command(docker_run_command, pem_file, instance_user_name, public_ip_address)

                

                return {'build_status': f"redis  completed successfully, running on {public_ip_address}", 'public_ip': public_ip_address}
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
def run_remote_command(command, pem_file, instance_user_name, public_ip_address):
        ssh_command = ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', pem_file,
                    f"{instance_user_name}@{public_ip_address}"] + command
        try:
         result = subprocess.run(ssh_command, check=True, capture_output=True, text=True)
         return result.stdout.strip()
        except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password