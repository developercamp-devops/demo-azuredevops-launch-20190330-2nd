import os
from .common import *

DEBUG = True

INSTALLED_APPS += ['storages']

STATICFILES_STORAGE = 'devops.storages.StaticS3Boto3Storage'
DEFUALT_FILE_STORAGE = 'devops.storages.MediaS3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('EB_APPLICATION_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'ap-northeast-2')

AWS_QUERYSTRING_AUTH = False

