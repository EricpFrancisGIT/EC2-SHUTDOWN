import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]

    # Check if event has query parameters
    if 'queryStringParameters' in event and event['queryStringParameters']:
        for key, value in event['queryStringParameters'].items():
            filters.append({'Name': f'tag:{key}', 'Values': [value]})
    else:
        # Default to Environment=Dev
        filters.append({'Name': 'tag:Environment', 'Values': ['Dev']})

    response = ec2.describe_instances(Filters=filters)

    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Stopped instances: {instance_ids}")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("No matching running instances found.")
        }
