import boto3
import json

ec2 = boto3.resource('ec2', region_name='us-east-1')

def lambda_handler(event, context):
    filteredInstances = []

    ec2Filters = [
        {
            'Name': 'tag:Environment',
            'Values': ['DEV']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }]
    

    instances = ec2.instances.filter(Filters=ec2Filters)

    for instance in instances:
        filteredInstances.append(instance.id)

        print(filteredInstances)

    positiveMessage = f"Congratulations! The following {len(filteredInstances)} instances have been stopped."
    negativeMessage = "There are no instances matching with the selected filters. Please adjust filters and try again."
    



