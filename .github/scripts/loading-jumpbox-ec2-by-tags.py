import boto3
import json
import os

def get_ec2_instances_by_tags(tags):
    ec2 = boto3.client('ec2')
    filters = [{'Name': f'tag:{k}', 'Values': [v]} for k, v in tags.items()]

    response = ec2.describe_instances(Filters=filters)

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)

    return instances


tags = {
    'Name': os.environ['NAME'],
    'JumpBox': 'true',
    'Vpc': os.environ['VPC_NAME'],
}
instances = get_ec2_instances_by_tags(tags)
result = {'instances': instances}
with open('ec2_instances.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)
print(f"Found {len(instances)} instances. Results saved to ec2_instances.json")
