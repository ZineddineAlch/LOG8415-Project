import boto3

client = boto3.client('lambda')
response = client.add_permission(
    FunctionName='lambdafunctprojet1',
    StatementId='MyString1',
    Action='lambda:InvokeFunction',
    Principal="apigateway.amazonaws.com",
    SourceArn="arn:aws:lambda:us-east-1:713669503309:function:lambdafunctprojet1"
)

print(response)