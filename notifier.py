import boto3
import os
import stat
import requests

session = boto3.Session(profile_name='eureka-terraform', region_name='us-east-1')
ec2 = session.resource('ec2')

key_name = 'python_automation_key'
key_path = "/Users/kevinmcgarry/.ssh/" + key_name + '.pem'

# create keypair in AWS
key = ec2.create_key_pair(KeyName=key_name)

# to view the private key stored in AWS
# key.key_material

# create pem key locally containing private key data
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)

# modifying the permissions on the pem key on the local system
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)

# AMI Related
img = ec2.Image('ami-04681a1dbd79675a5')  # pull ami id from website
ami_name = img.name  # grab ami's name (different than id) and assign to ami_name

# EC2 Related
# Create instances and assign to instances object (which is a list of ec2 instances created)
# Note when using a non-default VPC, must use SecurityGroupIds
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro',
                                 SubnetId='subnet-fae968d1', SecurityGroupIds=['sg-0fdf54fefddc82180'],
                                 KeyName=key.key_name)
inst = instances[0]  # assign instance to inst object
inst.reload()  # refresh data attributes of inst object
# inst.public_ip_address  # get public ip address
# inst.public_dns_name  # get public dns entry of instance

# terminate the instance
# inst.terminate()

# SG Related
# display list of security groups instance is a part of
# output is a list of dictionaries, each dict containing one SG
# inst.security_groups

# create SG object
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])

# create rule in SG to allow ssh and http from local office
sg.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol': 'TCP',
                                     'IpRanges': [{'CidrIp': '71.42.237.146/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol': 'TCP',
                                     'IpRanges': [{'CidrIp': '71.42.237.146/32'}]}])



# AutoScaling Related
as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups()  # get a list of ASGs for this region
as_client.describe_auto_scaling_groups(AutoScalingGroupNames=['Notifier_ASG'])
as_client.execute_policy(AutoScalingGroupName='Notifier_ASG', PolicyName='Scale Out')

