import boto3
import time

AWS_REGION = 'us-east-1'
instance_name = 'project'
answer = "NO"

while (answer == 'NO'):
    answer = input("Do you want to shutdown the system ?  YES or NO   ")
    time.sleep(10)

print('------------ Delete lambda function----------------')
client = boto3.client('lambda')
client.delete_function(FunctionName='lambdafunctprojet1')

print('------------ Delete S3 bucket----------------')
s3 = boto3.resource('s3')
client = boto3.client('s3')
PREFIX = 'Trained_data/'
response1 = client.list_objects_v2(Bucket='sagemaker-projecttp3', Prefix=PREFIX)

for object in response1['Contents']:
    print('Deleting', object['Key'])
    client.delete_object(Bucket='sagemaker-projecttp3', Key=object['Key'])

s3.Object('sagemaker-projecttp3', 'data.csv').delete()

bucket = s3.Bucket('sagemaker-projecttp3')
bucket.delete()

def wait_until_stopping(instance_name,rn):
    """
    This function waits for the notebook instance to be stopped.
    instance_name: name of instance to be stopped.
    rn: region name.

    """
    while (True):
        sm_client = boto3.client("sagemaker", region_name=rn)
        response = sm_client.describe_notebook_instance(
            NotebookInstanceName=instance_name
        )
        if response["NotebookInstanceStatus"] == "Stopped":
            return print("Notebook in service")
        time.sleep(5)

def wait_until_deleting(instance_name,rn):
    """
     This function waits for the notebook instance to be deleted.
    instance_name: name of instance to be stopped.
    rn: region name.
    """
    while (True):
        sm_client = boto3.client("sagemaker", region_name=rn)
        response = sm_client.describe_notebook_instance(
            NotebookInstanceName=instance_name
        )
        if response["NotebookInstanceStatus"] == "Deleting":
            return print("Notebook in service")
        time.sleep(5)


print('------------ STOPPING Notebook instance ----------------')
client = boto3.client('sagemaker')
response = client.stop_notebook_instance(
    NotebookInstanceName='project')
wait_until_stopping(instance_name=instance_name, rn=AWS_REGION)
print('Instance Notebook Stopped...')

print('------------ DELETING Notebook instance----------------')
client = boto3.client('sagemaker')
client.delete_notebook_instance(NotebookInstanceName='project')
wait_until_deleting(instance_name=instance_name, rn=AWS_REGION)
print('Notebook instance deleted...')

print('------------DELETE API REST------------')
with open('api_id_store.txt') as f:
    URL = f.readlines()

client = boto3.client('apigateway')
client.delete_rest_api(
    restApiId=URL[0])
print('API REST deleted...')



