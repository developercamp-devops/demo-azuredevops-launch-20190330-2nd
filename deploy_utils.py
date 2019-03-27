import boto3
import sys
from datetime import datetime
import time


class ElasticBeanstalk:
    def __init__(self, application_name, solution_stack_name):
        self.client = boto3.client('elasticbeanstalk')
        self.s3_client = boto3.client('s3')
        self.application_name = application_name
        self.solution_stack_name = solution_stack_name

    def create_application_if_not_exists(self):
        response = self.client.describe_applications(ApplicationNames=[self.application_name])
        if (not response['Applications']) or (response['Applications'][0]['ApplicationName'] != self.application_name):
            response = self.client.create_application(ApplicationName=self.application_name)
            return response

    def upload_archive(self, file_path):
        s3_bucket_name = self.client.create_storage_location()['S3Bucket']
        version_label = 'app-' + datetime.now().strftime('%y%m%d_%H%M%S')
        s3_local_path = '/'.join([self.application_name, version_label + '.zip'])
        self.s3_client.upload_file(file_path, s3_bucket_name, s3_local_path)
        return s3_bucket_name, s3_local_path, version_label

    def create_application_version(self, s3_bucket_name, s3_local_path, version_label):
        response = self.client.create_application_version(
                ApplicationName=self.application_name,
                VersionLabel=version_label,  # FIXME: 필히 Unique해야함.
                SourceBundle = {
                    'S3Bucket': s3_bucket_name,
                    'S3Key': s3_local_path,
                },
            )
        return response

    def create_or_update_environment(self, environment_name, version_label, option_settings):
        response = self.client.describe_environments(
            ApplicationName=self.application_name,
            EnvironmentNames=[environment_name],
            IncludeDeleted=False,
        )
        if response['Environments']:
            response = self.client.update_environment(
                ApplicationName=self.application_name,
                EnvironmentName=environment_name,
                VersionLabel=version_label,
                SolutionStackName=self.solution_stack_name,
                OptionSettings=option_settings,
            )
        else:
            response = self.client.create_environment(
                ApplicationName=self.application_name,
                EnvironmentName=environment_name,
                VersionLabel=version_label,
                SolutionStackName=self.solution_stack_name,
                Tags = [ {'Key': 'name', 'Value': environment_name}, ],
                OptionSettings=option_settings,
            )
        environment_id = response['EnvironmentId']

        return environment_id

    def get_environment_status(self, environment_id):
        response = self.client.describe_environments(
            ApplicationName=self.application_name,
            EnvironmentIds=[environment_id],
            IncludeDeleted=False,
        )
        for env in response['Environments']:
            if env['EnvironmentId'] == environment_id:
                return {
                    'Status': env['Status'],
                    'Health': env['Health'],
                }

        return None

    @classmethod
    def deploy(cls, application_name, environment_name, solution_stack_name, archive_file_path, option_settings):
        eb = cls(application_name, solution_stack_name)
        eb.create_application_if_not_exists()

        print('upload archive ...')
        s3_bucket_name, s3_local_path, version_label = eb.upload_archive(archive_file_path)
        print('s3_bucket_name :', s3_bucket_name)
        print('s3_local_path :', s3_local_path)
        print('version_label :', version_label)

        print('create application version ...')
        eb.create_application_version(s3_bucket_name, s3_local_path, version_label)

        print('create/update environment ...')
        environment_id = eb.create_or_update_environment(environment_name, version_label, option_settings)
        print('environment_id:', environment_id)

        print('check environment status ...')
        for _ in range(100):
            time.sleep(3)
            status = eb.get_environment_status(environment_id)
            if status is None:
                print('ERROR: not found environment:', environment_id)
                break
            print('Status: {Status}, Health: {Health}'.format(**status))

            if status['Status'] == 'Ready':  # Green, Yellow, Red, Grey
                print('INFO: create/update environment:', environment_name)
                break
        else:
            print('ERROR: environment %s failed to transition to healthy state' % environment_name)
            sys.exit(1)

