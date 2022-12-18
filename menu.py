import boto3
import sys

'''
print('------------ Delete lambda function----------------')
client = boto3.client('lambda')
client.delete_function(FunctionName='lambdafunctprojet1')
print('------------ Delete API Gateway----------------')
with open('api_id_store.txt') as f:
    URL = f.readlines()
client = boto3.client('apigateway')
response = client.delete_rest_api(
    restApiId=URL[0]
)

print('------------ Delete IAM Role----------------')
client = boto3.client('iam')
response = client.delete_role(
    RoleName='roleprojectlambda'
)
response = client.delete_role(
    RoleName='roleprojectsagemaker'
)
'''
'''
print('------------ Delete S3 bucket----------------')
s3 = boto3.resource('s3')
client = boto3.client('s3')
objects = client.list_objects_v2(Bucket='sagemaker-projecttp3')


client.delete_object(
    Bucket='sagemaker-projecttp3',
    Key='Trained_data/'
)

PREFIX = 'Trained_data/'
response1 = client.list_objects_v2(Bucket='sagemaker-projecttp3', Prefix=PREFIX)
for object in response1['Contents']:
    print('Deleting', object['Key'])
    client.delete_object(Bucket='sagemaker-projecttp3', Key=object['Key'])


bucket = s3.Bucket('sagemaker-projecttp3')
bucket.delete()
'''
'''
print('------------ Stopping Notebook instance----------------')
client = boto3.client('sagemaker')
response = client.stop_notebook_instance(
    NotebookInstanceName='project'
)
'''
'''
print('------------ Delete Notebook instance----------------')
client = boto3.client('sagemaker')
response = client.delete_notebook_instance(NotebookInstanceName='project')
'''


# Specify your AWS Region
aws_region='us-east-1'

# Specify the name of your endpoint
endpoint_name='DEMO-linear-endpoint-202212172128'

# Create a low-level SageMaker service client.
sagemaker_client = boto3.client('sagemaker', region_name=aws_region)

# Delete endpoint
sagemaker_client.delete_endpoint(EndpointName=endpoint_name)


'''
def shutdown_system(instances_ids):
    """
    This function shutdows the system.
    ids : the IDs of the instances that needs to be shut down.
    """
    print('Shutting down system...')
    terminate_instance(instances_ids)
    wait_for_instance_terminated(instances_ids)
    delete_sg()
    print('System shutdown.')


id_list = [id]
while True:
    print('\nMenu :')
    print('    press \'i\' to get informations. ')
    print('    press \'q\' to quit. ')
    print('    press \'s\' to shutdown everything. ')
    line = input('> ')
    if (line == 'i'):
        print('\nRunning instances :')
        id_list = get_running_instances()
    elif (line == 'q'):
        sys.exit()
    elif (line == 's'):
        shutdown_system(id_list)
    elif (line == ''):
        continue
    else:
        print('Unknown commad.')

'''



