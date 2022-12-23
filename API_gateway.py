import time
import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)
client = boto3.client('apigateway')

def get_account_id():
    """
    Function to get AWS account id
    """
    client = boto3.client("sts")
    return client.get_caller_identity()["Account"]


def create_rest_api(api_name):
    """
    Function to create REST API
    api_name: name of the API
    """
    client = boto3.client('apigateway')
    response = client.create_rest_api(
        name=api_name,
        endpointConfiguration={
            'types': [
                'REGIONAL',
            ]
        }
    )
    return response["id"]

def create_resource(api_id):

    client = boto3.client('apigateway')
    resources = client.get_resources(restApiId=api_id)

    root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

    D=client.create_resource(restApiId=api_id, parentId=root_id, pathPart="Resource")
    return D

def create_put_method(api_id,D):
    client = boto3.client('apigateway')
    client.put_method(
    restApiId=api_id,
    resourceId=D['id'],
    httpMethod="POST",
    authorizationType="none",
    requestParameters={"method.request.header.InvocationType": True}
    )

def create_put_method_response(api_id,D):
    client = boto3.client('apigateway')
    client.put_method_response(
        restApiId=api_id, resourceId=D['id'], httpMethod="POST", statusCode="200"
    )

time.sleep(10)

def create_put_integration(api_id,D):
    client = boto3.client('apigateway')

    client.put_integration(
        restApiId=api_id,
        resourceId=D['id'],
        httpMethod="POST",
        type='AWS',
        uri='arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:{}:function:lambdafunctprojet1/invocations'.format(account_id),
        integrationHttpMethod="POST",
        credentials="arn:aws:iam::{}:role/roleprojectlambda".format(account_id)

    )
def create_put_integration_response(api_id,D):
    client = boto3.client('apigateway')

    client.put_integration_response(
        restApiId=api_id,
        resourceId=D['id'],
        httpMethod='POST',
        statusCode="200",
        responseTemplates={}
    )

stage_name = "dev"
def deploy_api(stage_name,api_id):
    """
    Deploys a REST API. After a REST API is deployed, it can be called from any
    REST client, such as the Python Requests package or Postman.
    :param stage_name: The stage of the API to deploy, such as 'test'.
    :return: The base URL of the deployed REST API.
    """
    client = boto3.client("apigateway")
    try:
        client.create_deployment(
            restApiId=api_id, stageName=stage_name)
        stage = stage_name
        logger.info("Deployed stage %s.", stage_name)
    except ClientError:
        logger.exception("Couldn't deploy stage %s.", stage_name)
        raise
    else:
        return api_url()

def api_url(stage_name=stage_name,resource=None):
    """
    Builds the REST API URL from its parts.
    :param resource: The resource path to append to the base URL.
    :return: The REST URL to the specified resource.
    """
    client = boto3.client("apigateway")
    url = (f'https://{api_id}.execute-api.{client.meta.region_name}'
           f'.amazonaws.com/{stage_name}''/Resource')
    if resource is not None:
        url = f'{url}/{resource}'
    return url

api_name = 'BreastCancerPredition_API'
account_id = get_account_id()
print('------------------Create REST API---------------------')
api_id = create_rest_api(api_name)
with open('api_id_store.txt', 'w') as f:
    f.write(api_id)
f.close()

D = create_resource(api_id)
create_put_method(api_id,D)
create_put_method_response(api_id,D)
create_put_integration(api_id,D)
create_put_integration_response(api_id,D)
time.sleep(10)
print('REST API created...')
print('---------------Deploy REST API---------------')
api_url = deploy_api(stage_name="dev",api_id=api_id)

with open('api_url_store.txt', 'w') as f:
    f.write(api_url)
f.close()
time.sleep(10)
print('REST API deployed...')