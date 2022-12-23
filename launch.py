import os
import time
os.system("IAM_sagemaker.py")
os.system("IAM_lambda.py")
os.system("file_zip.py")
os.system("lambda_function.py")
os.system("create_S3_bucket.py")
os.system("sagemaker_instance.py")
os.system("API_gateway.py")
os.system("Request.py")
time.sleep(10)
os.system("menu.py")
time.sleep(20)

