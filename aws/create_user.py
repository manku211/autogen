import os,time,json
import boto3
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Type

load_dotenv(".env")

create_user_json = {
    "user_name": {
        "description": "provide the user_name",
        "type": "Required",
    },
    "project_name": {
        "description": "provide the project_name",
        "type": "Required",
    }
}
class CreateUserInput(BaseModel):
    user_name: str = Field(description="should be a string")
    project_name: str = Field(description="should be a string")

class CreateUser(BaseModel):
    name = "create_user"
    description = "create user in aws with the bucket of project name"
    args_schema: Type[BaseModel] = CreateUserInput

    region = os.getenv('REGION')
    access_key = os.getenv('ACCESS_KEY')
    secret_key = os.getenv('SECRET_KEY')
    
    

    def create_user(self,user_name: str,project_name: str):
        current_epoch_time = get_current_epoch_time()
        bucket_name = f'{project_name}-{current_epoch_time}'
        print(bucket_name)
        iamboto=boto3.client(
                'iam',
                region_name=os.getenv('REGION'),
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY')
            )
        
        try:
            user_response=iamboto.create_user( UserName=user_name)
            print(f"Created user: {user_response['User']['UserName']}")
            keys_response = iamboto.create_access_key(UserName=user_name)
            access_key = keys_response['AccessKey']['AccessKeyId']
            secret_key = keys_response['AccessKey']['SecretAccessKey']
            print(f"Access Key: {access_key}")
            print(f"Secret Key: {secret_key}")
            res=create_bucket(bucket_name,user_name)
        except Exception as e:
                    print(f"Failed to create user '{user_name}': {e}")
                    return False

        #print("res:",res[0])
        result_list = list(res.items())
        arn_key, arn_value = result_list[0]
        print(arn_value)
        

        print(f"Attached policy {arn_value} to user {user_name}")
        return {'creation of user with attach policy with bucket name': f"user_name {user_name}", "with access key":access_key,"and secret key":secret_key,"with bucket name":bucket_name ,"attach policy":arn_value}


def get_current_epoch_time():
        return int(time.time()) 


def create_bucket(bucket_name:str,user_name: str):
      
        s3boto=boto3.client(
                's3',
                region_name=os.getenv('REGION'),
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY')
            )
        iamboto=boto3.client(
                'iam',
                region_name=os.getenv('REGION'),
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY')
            ) 
        try:  
            s3boto.create_bucket(Bucket=bucket_name)
            print(f"Created bucket: {bucket_name}")
            response = s3boto.put_public_access_block(Bucket=bucket_name,PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            })
        except Exception as e:
            print(f"Failed to create bucket '{bucket_name}': {e}")
            return False
        print(response)
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        bucket_policy_json = json.dumps(policy_document)
        s3boto.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json) 
        user_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        policy_response = iamboto.create_policy(
            PolicyName=f'{user_name}_s3_rw_policy',
            PolicyDocument=json.dumps(user_policy)
        )

        policy_arn = policy_response['Policy']['Arn']
        print(f"Created policy with ARN: {policy_arn}")
        iamboto.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn)
        return {'creation of user with attach policy with bucket name':policy_arn}
        
