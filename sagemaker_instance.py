import boto3
import time
import webbrowser
AWS_REGION = 'us-east-1'
instance_type = 'ml.t2.medium'
instance_name = 'project'

client = boto3.client('iam')
response = client.get_role(
    RoleName='roleprojectsagemaker')
def get_vpc_id_and_subnet_id(rn):

    """
    This function returns the id of the default vpc and of the first subnet.
    Returns vpc_id, subnet_id.
    """
    ec2_client = boto3.client("ec2", region_name=rn)
    response = ec2_client.describe_vpcs()
    vpc_id = response['Vpcs'][0]['VpcId']
    response = ec2_client.describe_subnets(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
    )
    subnet_id = response['Subnets'][0]['SubnetId']
    return vpc_id, subnet_id
def create_sg(vpcID,rn):
    """
    This function creates a new security group for the VPC.
    vpcID : is the ID of the concerned VPC.
    Returns the security group ID.
    """
    ec2_client = boto3.client("ec2", region_name=rn)
    response = ec2_client.create_security_group(GroupName="Project",
                                                Description='SG_basic',
                                                VpcId=vpcID)
    security_group_id = response['GroupId']
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},

        ])
    return security_group_id
def create_notebook_instance(instance_name,instance_type,subnet_id,sg, rn,role_arn):
    """
    This function creates sagemaker instance.
    instance_name : is the name desired of instance to be created.
    instance_type : the instance type. ml.t2.medium for our example.
    sg_id : is the ID of the security group that you wish your instace to follow.
    subnet_id : is the subnet where you instances will reside.
    rn: the region name
    """
    sm_client = boto3.client("sagemaker", region_name=rn)
    sm_client.create_notebook_instance(
        NotebookInstanceName=instance_name,
        InstanceType=instance_type,
        SubnetId=subnet_id,
        SecurityGroupIds=[
            sg,
        ],
        RoleArn=role_arn,
        Tags=[
            {
                'Key': 'MLtest',
                'Value': '12345'
            },
        ]
    )
def wait_until_running(instance_name,rn):
    """
    This function waits for the notebook instance to become available.
    """
    while (True):
        sm_client = boto3.client("sagemaker", region_name=rn)
        response = sm_client.describe_notebook_instance(
            NotebookInstanceName=instance_name
        )
        if response["NotebookInstanceStatus"] == "InService":
            return print("Notebook in service")
        time.sleep(5)

def open_notebook(instance_name):

    client = boto3.client('sagemaker')
    response = client.create_presigned_notebook_instance_url(
        NotebookInstanceName=instance_name
    )
    webbrowser.open(response['AuthorizedUrl'])
    time.sleep(10)



print("------------------- Creating SageMaker instance ----------------------")

print("Retrieving role Arn from IAM role...")
role_arn = response['Role']['Arn']

print("Getting the vpc and the subnet IDs...")
vpcID, subnet_id = get_vpc_id_and_subnet_id(rn=AWS_REGION)
print("IDs obtained!")

print("Creating the security group...")
sg_id = create_sg(vpcID, rn=AWS_REGION)
print("Security group created!\n")

print("Creating the Sagemaker instance type ml.t2.medium ...")
create_notebook_instance(instance_name=instance_name, instance_type=instance_type, subnet_id=subnet_id, sg=sg_id, rn=AWS_REGION, role_arn=role_arn)
print("Sagemaker instance created...\n")

print("Waiting for the Sagemaker instance to get in the running state...This action takes few minutes to complete. Be patient !")
wait_until_running(instance_name=instance_name, rn=AWS_REGION)
print("Notebook instance is running!. UPLOAD THE CODE TO SAGEMAKER")

print("Opening SageMaker Notebook...")
open_notebook(instance_name)
print("SageMaker Notebook opened...")

answer = 'NO'
while (answer == 'NO'):
    answer = input("Did you UPLOAD and RUN Notebook ?  YES or NO   ")
    time.sleep(15)


