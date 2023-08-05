"""
Module to download git repo and upload it to Amazon s3
Configure the bucket, and git url using the settings file
Ths also requires AWS credentials to be set up in a file (or using AWS CLI):
Unix: ~/.aws/credentials
Windows: C:\\Users\\Username\\.aws\\credentials
In this file put the following:
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
[default]
region=us-east-1
"""

import os
import boto3
import stat
import sys
from utils import upload_dir, push_project_to_s3


def remove_readonly(func, path, excinfo):
    """
    Changes permissions on files that can't be deleted
    by shutil.rmtree
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


if __name__ == "__main__":
    if not sys.argv[1]:
        logger.critical('You must provide a directory to push!')
        exit(1)

    s3_resource = boto3.resource('s3')
    push_project_to_s3(sys.argv[1], sys.argv[2])
# OLD for cloning and pushing
#
# # Create temp directory
# print("Creating temporary directory %s" % settings.TEMP_DIRECTORY)
# if not os.path.exists(settings.TEMP_DIRECTORY):
#     os.makedirs(settings.TEMP_DIRECTORY)
# # Clone repository to temp directory
# print("Cloning repository from %s" % settings.GIT_URL)
# Repo.clone_from(settings.GIT_URL, settings.TEMP_DIRECTORY)
#
# # Uploads contents of temp directory to s3
# print("Uploading to S3")
# upload_dir(settings.TEMP_DIRECTORY)
#     finally:
#         # Deletes temporary directory
#         print("Deleting temporary directory and contents")
#         shutil.rmtree(settings.TEMP_DIRECTORY, onerror=remove_readonly)