import boto3
import os
from dotenv import load_dotenv
load_dotenv(".env")

def get_instance_name(ec2_client, instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    
    # Extract the instance name from the tags
    for tag in instance['Tags']:
        if tag['Key'] == 'Name':
            return tag['Value']
    return None

def allocate_and_associate_eip(instance_id):
    # Create a boto3 EC2 client
    ec2_client = boto3.client(
            'ec2',
            region_name=os.getenv('REGION'),
            aws_access_key_id=os.getenv('ACCESS_KEY'),
            aws_secret_access_key=os.getenv('SECRET_KEY')
        )

    try:
        instance_name = get_instance_name(ec2_client, instance_id)
        if not instance_name:
            print(f"No 'Name' tag found for instance {instance_id}")
            return
        allocation = ec2_client.allocate_address(Domain='vpc')
        allocation_id = allocation['AllocationId']
        elastic_ip = allocation['PublicIp']
        print(f"Allocated Elastic IP with Allocation ID: {allocation_id}")

        # Associate the Elastic IP address with the specified EC2 instance
        association = ec2_client.associate_address(
            InstanceId=instance_id,
            AllocationId=allocation_id
        )
        association_id = association['AssociationId']
        print(f"Associated Elastic IP with Association ID: {association_id}")
        ec2_client.create_tags(
            Resources=[allocation_id],
            Tags=[{'Key': 'Name', 'Value': instance_name}]
        )
        print(f"Tagged Elastic IP with Name: {instance_name}")
        return elastic_ip

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Replace 'your_instance_id_here' with your actual EC2 instance ID
instance_id = 'i-0eb885b1e937d0772'
allocate_and_associate_eip(instance_id)

