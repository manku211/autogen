import os
import boto3
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type
from typing import Annotated

load_dotenv(".env")

create_vpc_json = {
    "vpc_name": {
        "description": "Name of the VPC",
        "type": "Required",
    },
    "vpc_cidr_block": {
        "description": "CIDR Block of the VPC",
        "type": "Required",
    },
}


class CreateVpcInput(BaseModel):
    vpc_name: str = Field(description="should be a string")
    vpc_cidr_block: str = Field(description="should be a string")

class CreateVpc(BaseModel):
    name = "create_vpc"
    description = "Initiate the function when user asks to create vpc"
    args_schema: Type[BaseModel] = CreateVpcInput

    region = os.getenv('REGION')
    access_key = os.getenv('ACCESS_KEY')
    secret_key = os.getenv('SECRET_KEY')

    def create_vpc(self, vpc_cidr_block: str, vpc_name: str):
        ec2 = boto3.client(
            'ec2',
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

        # Create VPC
        vpc_response = ec2.create_vpc(CidrBlock=vpc_cidr_block)
        vpc_id = vpc_response['Vpc']['VpcId']

        # Add a name tag to the VPC
        ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])

        return { "vpc_id": vpc_id }

    def delete_vpc(self, vpc_id):
        ec2 = boto3.client(
            'ec2',
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

        ec2.delete_vpc(VpcId=vpc_id)
        print(f"Deleted VPC {vpc_id}")    



