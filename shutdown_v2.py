def stop_dev_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'tag:Environment', 'Values': ['Dev']}
    ])

    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if instance_ids:
        print(f"Stopping Dev instances: {instance_ids}")
        ec2.stop_instances(InstanceIds=instance_ids)
    else:
        print("No running Dev instances found.")
