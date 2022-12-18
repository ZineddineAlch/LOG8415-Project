import json
import boto3
import time
role_name = 'roleprojectlambda'

assume_policy = json.dumps(
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com",
                    "apigateway.amazonaws.com","sagemaker.amazonaws.com","s3.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
})


client = boto3.client('iam')
print('-------------------Create role--------------')

response = client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=assume_policy)

print('------------------Role created--------------')

print('-------------------Add role policy--------------')
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

response6= client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess'
)

print('-------------------Role policy added--------------')

time.sleep(10)