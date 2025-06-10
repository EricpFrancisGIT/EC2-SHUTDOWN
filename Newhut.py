import boto3
import json

ec2 = boto3.resource('ec2', region_name='us-east-1')

def lambda_handler(event, context):
    filteredInstances = []

    ec2Filters = [
        {
            'Name': 'tag:Environment',
            'Values': ['Dev']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }]

    # get instances by tag and 'running' state
    instances = ec2.instances.filter(Filters=ec2Filters)