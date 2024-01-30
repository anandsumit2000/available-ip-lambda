import boto3
import os

def get_available_ips(vpc_id):
    ec2 = boto3.client("ec2")

    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = response['Subnets']

    available_ips = []
    
    for subnet in subnets:
        subnet_id = subnet['SubnetId']

        available_ips_count = subnet.get('AvailableIpAddressCount', 0)
        available_ips.append((subnet_id, available_ips_count))
    
    return available_ips

def lambda_handler(event, context):
    # Set your VPC ID here
    vpc_id = os.environ.get('VPC_ID')

    if not vpc_id:
        return {
            'statusCode': 400,
            'body': {
                'message': 'VPC_ID environment variable is not set.'
            }
        }

    available_ips = get_available_ips(vpc_id)

    print("Available IPs in the VPC:")
    for subnet_id, ips_count in enumerate(available_ips, start=1):
        print(f"Subnet {subnet_id}: {ips_count[1]} IPs")

    return {
        'statusCode': 200,
        'body': {
            'message': 'Available IPs in the VPC',
            'available_ips': available_ips
        }
    }