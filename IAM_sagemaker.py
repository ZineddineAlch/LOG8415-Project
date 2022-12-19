import json
import boto3

role_name = 'roleprojectsagemaker'

assume_policy = json.dumps(
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": ["sagemaker.amazonaws.com","apigateway.amazonaws.com"]
            },
            "Action": "sts:AssumeRole"
        }
    ]
})


client = boto3.client('iam')
print('--------------SageMakerCreate role--------------')

response = client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=assume_policy)

print('Role created...')

print('-------------------Add role policies--------------')

response2 = client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess')

response3 = client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AWSLambda_FullAccess'
)
response4= client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AWSLambdaExecute'
)
response5= client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaRole'
)
print('Role policies added...')