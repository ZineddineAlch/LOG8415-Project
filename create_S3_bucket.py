import logging
import boto3
from botocore.exceptions import ClientError
import time
import os

bucket_name = 'sagemaker-projecttp3'  # The name must start with lowercase letter
def create_bucket(bucket_name, region=None):

    """Create an S3 bucket in a specified region
    bucket_name: Bucket to create
    region: String region to create bucket in, e.g., 'us-west-2'
    return: True if bucket created, else False
    """

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):

    """Upload a file to an S3 bucket
    file_name: File to upload
    bucket: Bucket to upload to
    object_name: S3 object name. If not specified then file_name is used
    return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

print("---------------- Creating S3 bucket and upload dataset----------------")
create_bucket(bucket_name=bucket_name, region=None) # The name of bucket should start with lowercase letter
print("Uploading dataset to S3 bucket...")
upload_file('data.csv', bucket_name)
time.sleep(10)
print("Dataset uploaded...")
