import boto3
import json
import os

def get_security_groups_by_tags(tags):
    ec2 = boto3.client('ec2')
    filters = [{'Name': f'tag:{k}', 'Values': [v]} for k, v in tags.items()]

    response = ec2.describe_security_groups(Filters=filters)

    security_groups = response['SecurityGroups']

    return security_groups


tags = {
    'Name': os.environ['NAME'],
    'JumpBox': 'true',
    'Vpc': os.environ['VPC_NAME'],
}
security_groups = get_security_groups_by_tags(tags)
result = {'security_groups': security_groups}
with open('security_groups.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)
print(f"Found {len(security_groups)} security groups. Results saved to security_groups.json")
