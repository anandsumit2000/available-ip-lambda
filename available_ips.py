import os
import boto3

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

def push_metric_to_cloudwatch(metric_name, value, namespace='VPCCustomNamespace'):
    cloudwatch = boto3.client('cloudwatch')

    subnet_id, ips_count = value

    # Put metric data
    cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': ips_count,
                'Unit': 'Count',
                'Dimensions': [{'Name': 'SubnetId', 'Value': subnet_id}]
            },
        ]
    )

# def lambda_handler(event, context):
# event and context parameters have no utilization in this script
# as a result pylint raises an W0613 (unused arguments in your function or method)
# hence they have been replaced with _ and __ to allow
# AWS Lambda to trigger the function

def lambda_handler(_, __):
    # Set your VPC ID as environment variable
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

        # Push metric to CloudWatch
        push_metric_to_cloudwatch('Available IP Count', ips_count)

    return {
        'statusCode': 200,
        'body': {
            'message': 'Available IPs in the VPC',
            'available_ips': available_ips
        }
    }
