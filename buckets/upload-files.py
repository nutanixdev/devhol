#!/usr/local/bin/python

import boto3
import glob
import re

# user defined variables
endpoint_ip= "<your-endpoint-ip>"
access_key_id="<access-key>"
secret_access_key="<secret-key>"
bucket="<bucket-name-to-upload-to>"
name_of_dir="sample-files"

# system variables
endpoint_url= "https://"+endpoint_ip+":7200"
filepath = glob.glob("%s/*" % name_of_dir)

# connect to object store
session = boto3.session.Session()
s3client = session.client(service_name="s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, endpoint_url=endpoint_url, verify=False)

# go through all the files in the directory and upload
for current in filepath:
  full_file_path=current
  m=re.search('sample-files/(.*)', current)
  if m:
    object_name=m.group(1)
  print("Path to File:",full_file_path)
  print("Object name:",object_name)
  response = s3client.put_object(Bucket=bucket, Body=full_file_path, Key=object_name)
#     print(response)
