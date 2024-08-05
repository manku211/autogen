import os,json
from dotenv import load_dotenv
import subprocess
import json


load_dotenv(".env")

def run_terraform(directory):
    print("running terraform")
    commands = [
        ['terraform', 'init','-backend-config=backend.tfvars'],
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
    try:
        result = subprocess.run(
            ['terraform', 'output', '-json'],
            check=True,
            capture_output=True,
            text=True,
            cwd=directory
        )
        outputs = json.loads(result.stdout)
        instance_id = outputs['instance_id']['value']
        public_ip = outputs['public_ip']['value']
        return instance_id, public_ip
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(e.stderr)
        return False 


class CreateBacknd():
    " create ec2 backend "
    description = "create backend with the ec2"
    region  =     os.getenv('REGION')
    access_key = os.getenv('ACCESS_KEY')
    secret_key = os.getenv('SECRET_KEY')

    def create_backend(self,bucket: str,project_name: str,environment: str,key_name: str,cidr_block: str='',vpc_id: str=''):
        key= "backend/terraform.tfstate"
        data = {
        'bucket': bucket,
        'key': key,    
        'access_key' : self.access_key,
        'secret_key' : self.secret_key,
        'region'  : self.region,    
        'project_name': project_name,
        'environment' : environment,
        'cidr_block' : cidr_block,
        'vpc_id' : vpc_id,
        'key_name' : key_name
        }
        
        filtered_keys_backend = ['bucket', 'key', 'access_key', 'secret_key', 'region']
        filtered_data_backend = {k: data[k] for k in filtered_keys_backend}
        filtered_keys_terraform = ['access_key', 'secret_key', 'region', 'project_name', 'environment', 'cidr_block', 'vpc_id','key_name']
        filtered_data_terraform = {k: data[k] for k in filtered_keys_terraform}
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(script_dir)
        relative_path_terraform = 'terraform/terraform-backend/root/terraform.auto.tfvars'
        relative_path_backend = 'terraform/terraform-backend/root/backend.tfvars'
        autogen_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        tf_file = os.path.join(autogen_dir, relative_path_terraform)
        tf_backend = os.path.join(autogen_dir,relative_path_backend)

        os.makedirs(os.path.dirname(tf_file), exist_ok=True)
        os.makedirs(os.path.dirname(tf_backend), exist_ok=True)
        with open(tf_file, 'w') as terraform_file:
            for key, value in filtered_data_terraform.items():
                terraform_file.write(f'{key} = "{value}"\n')

        # Write the filtered data to backend.tfvars
        with open(tf_backend, 'w') as backend_file:
            for key, value in filtered_data_backend.items():
                backend_file.write(f'{key} = "{value}"\n')
        terraform_directory = 'terraform/terraform-backend/root'
        terraform_directory_realtive_path = os.path.join(autogen_dir, terraform_directory)
        instance_id,public_ip=run_terraform( terraform_directory_realtive_path)
        return {'creation of backend done with the': f"instance_id {instance_id}", "public_ip":public_ip} 
inst = CreateBacknd()   

render=inst.create_backend("terraform-project-tfstatess","test-project","dev","my-key","10.6.0.0/16")

print(render)    
    