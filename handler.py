import os
import io
import boto3
import json
import csv

client = boto3.client('sagemaker')
response = client.list_endpoints(
    SortBy='Name',
    SortOrder='Ascending',
    StatusEquals='InService'
)
# grab environment variables
ENDPOINT_NAME = response['Endpoints'][0]['EndpointName']
runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)

    result = json.loads(response['Body'].read().decode())

    pred = int(result['predictions'][0]['score'])
    predicted_label = 'Malignant' if pred == 1 else 'Benign'

    return predicted_label
