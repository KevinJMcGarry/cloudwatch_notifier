"""Script for quickly running the scale out policy for an ASG."""

import boto3

session = boto3.Session(profile_name='eureka-terraform', region_name='us-east-1')
as_client = session.client('autoscaling')
#as_client.describe_auto_scaling_groups()  # get a list of ASGs for this region
#as_client.describe_auto_scaling_groups(AutoScalingGroupNames=['Notifier_ASG'])
response = as_client.execute_policy(AutoScalingGroupName='Notifier_ASG', PolicyName='Scale Out')
print(f"The operation returned an HTTP status code of {response['ResponseMetadata']['HTTPStatusCode']}")
