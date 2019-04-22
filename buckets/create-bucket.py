#!/usr/bin/python

import boto3
import warnings
warnings.filterwarnings("ignore")

endpoint_ip= "<object-store-ip>"
access_key_id="<access-key>"
secret_access_key="<secret-key>"
endpoint_url= "https://"+endpoint_ip+":7200"

session = boto3.session.Session()
s3client = session.client(service_name="s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, endpoint_url=endpoint_url, verify=False)

# Create Bucket
s3client.create_bucket(Bucket='<initials>-python-bob-bucket')

# list the buckets
response = s3client.list_buckets()

for b in response['Buckets']:
  print (b['Name'])
