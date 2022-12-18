import boto3
client = boto3.client('apigateway')
response = client.get_rest_api(
    restApiId='an46haes1k'
)
print(response)