def get_available_ips(vpc_id):
    

def lambda_handler(event, context):
    # Set your VPC ID here
    vpc_id = 'your_vpc_id'

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