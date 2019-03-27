#!/usr/bin/env python

import click
import os
import sys
from deploy_utils import ElasticBeanstalk


@click.command()
@click.option('--archive-file-path', required=True)
def main(archive_file_path):
    ElasticBeanstalk.deploy(
            application_name,
            environment_name,
            solution_stack_name,
            archive_file_path,
            option_settings)


if __name__ == '__main__':
    application_name = os.getenv('EB_APPLICATION_NAME', 'azure-devops-demo')
    environment_name = os.getenv('EB_ENVIRONMENT_NAME', 'stage')
    solution_stack_name = os.getenv('EB_SOLUTION_STACK_NAME',
            '64bit Amazon Linux 2018.03 v2.8.1 running Python 3.6')
    option_settings = [
        {
            'Namespace': 'aws:autoscaling:launchconfiguration',
            'OptionName': 'IamInstanceProfile',
            'Value': 'aws-elasticbeanstalk-ec2-role',
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'DJANGO_SETTINGS_MODULE',
            'Value': os.getenv('EB_DJANGO_SETTINGS_MODULE', 'devops.settings.prod'),
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'AWS_ACCESS_KEY_ID',
            'Value': os.getenv('EB_AWS_ACCESS_KEY_ID'),
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'AWS_SECRET_ACCESS_KEY',
            'Value': os.getenv('EB_AWS_SECRET_ACCESS_KEY'),
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'AWS_STORAGE_BUCKET_NAME',
            'Value': application_name,
        },
        {
            'Namespace': 'aws:elasticbeanstalk:container:python',
            'OptionName': 'WSGIPath',
            'Value': 'devops/wsgi.py',
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application',
            'OptionName': 'Application Healthcheck URL',
            'Value': os.getenv('EB_HEALTHCHECK_URL', '/'),
        }
    ]

    main()

