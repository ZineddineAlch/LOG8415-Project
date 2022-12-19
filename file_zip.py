import os
from zipfile import ZipFile


# Create a ZipFile Object
with ZipFile('lambda.zip', 'w') as zip_object:
   # Adding files that need to be zipped
   zip_object.write('handler.py')

# Check to see if the zip file is created
if os.path.exists('lambda.zip'):
   print("ZIP file for lambda function created...")
else:
   print("ZIP file not created...")