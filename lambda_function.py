import boto3
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')
role_name = 'roleprojectlambda'

print('---------------- Create lambda function--------------')
with open('lambda.zip', 'rb') as f:
    zipped_code = f.read()

role = iam_client.get_role(RoleName=role_name)


response = lambda_client.create_function(
    FunctionName='lambdafunctprojet1',
    Runtime='python3.9',
    Role=role['Role']['Arn'],
    Handler='handler.lambda_handler',
    Code=dict(ZipFile=zipped_code),
    Timeout=300,  # Maximum allowable timeout
)

print('----------------Lambda function created--------------')


