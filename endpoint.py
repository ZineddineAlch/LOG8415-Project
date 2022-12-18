import boto3

client = boto3.client('sagemaker')

response = client.list_endpoints(
    SortBy='Name',
    SortOrder='Ascending',
    StatusEquals='InService'
)
print(response['Endpoints'][0]['EndpointName'])