import boto3
import json

def lambda_handler(event, context):
    region_name = 'us-east-1'
    ec2_client = boto3.client('ec2', region_name=region_name)

    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    running_instances = []
    dev_instance_ids = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            is_dev = tags.get('Environment', '').lower() == 'dev'

            instance_info = {
                'InstanceId': instance_id,
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'Tags': tags
            }
            running_instances.append(instance_info)

            if is_dev:
                dev_instance_ids.append(instance_id)

    print("======These are the current Running Instances=======")
    for inst in running_instances:
        print(f"{inst['InstanceId']} ({inst['InstanceType']}) - State: {inst['State']}")
        print(f" Tags: {inst['Tags']}\n")

    if dev_instance_ids:
        print(f"Stopping Development instances: {dev_instance_ids}")
        ec2_client.stop_instances(InstanceIds=dev_instance_ids)
    else:
        print("No Development-tagged instances to stop.")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'StoppedInstances': dev_instance_ids,
            'TotalRunningInstances': len(running_instances)
        })
    }
    