#!/usr/bin/env python
import argparse
import json
import os
import datetime
from configparser import ConfigParser
import boto3
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AWSConnectionFactory:
    def __init__(self, environment, region, pod):

        self.env_map={'development' : 'nonprod',
                      'integration' : 'nonprod',
                      'production' : 'prod'}

        self.prod_map={'nonprod' : 0,
                       'prod' : 1}

        self.environment = environment
        self.region = region
        self.pod = pod

        self.get_assumed_credentials()


    def config(self, section):
        # create a parser
        parser = ConfigParser()
        # read config file
        configfile=os.path.join(os.path.expanduser('~'),'.aws','credentials')
        parser.read(configfile)

        settings = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                settings[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section))

        return settings

    def get_account_id(self):
        meta_account_id_url = 'https://metadata.aws.athenahealth.com/api/pods/?pod={}&is_prod={}'.format(self.pod,self.prod_map.get(self.env_map.get(self.environment)))
        req = requests.get(url=meta_account_id_url,  verify=False)
        response = req.text
        response_json = json.loads(response)
        return response_json.get('account_id')

    def get_assumed_credentials(self):
        credentials = self.config(self.env_map.get(self.environment))
        stsClient = boto3.client(
            'sts',
            region_name=self.region.replace('_','-'),
            aws_access_key_id = credentials.get('aws_access_key_id'),
            aws_secret_access_key = credentials.get('aws_secret_access_key')
        )
        account_id = self.get_account_id()
        assume_role_object = stsClient.assume_role(
            RoleArn='arn:aws:iam::{}:role/DataFabric'.format(account_id),
            RoleSessionName='sample'
        )

        credentials = assume_role_object.get('Credentials')
        self.access_key = credentials.get('AccessKeyId')
        self.secret_key = credentials.get('SecretAccessKey')
        self.session_token = credentials.get('SessionToken')
        return credentials



    def print_secrets(self):
        print(self.access_key + "," + self.secret_key)

    def get_client(self, resource):
        client = boto3.client(resource, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, aws_session_token=self.session_token, region_name="{}".format(self.region.replace('_','-')))
        return client

    def get_resource(self, resource):
        resource = boto3.resource(resource, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, aws_session_token=self.session_token, region_name="{}".format(self.region.replace('_','-')))
        return resource




class SSMInvoke(object):

    SUCCESS_STATES = ["Success"]
    ERROR_STATES = ["Failed"]
    ERROR_DETAIL_STATES = ["NoInstancesInTag"]
    STATES = ['Success', 'Failed', 'NoInstanceInTag']

    def __init__(self):
        """Object constructor, sets defaults."""
        self.targets = []
        self.command = None
        self.instances = []
        self.comment = ""
        self.ssm_client = None
        self.wait = False
        self.show_output = False
        self.deployement_key = ""
        self.bucket_name = ""
        self.pod=""
        self.environment=""
        self.region=""


    def get_pod_environment_from_deployment_key(self):
        """extract the pod, environment and region from deployment key"""
        parse_deployment_key = self.deployement_key.split('_')
        self.pod = parse_deployment_key[0]
        self.environment=parse_deployment_key[1]


    def parse_args(self, parsed_args):
        """Convert the argsparser arguments into the internal representation required for the SSM commands and logic flow.
        :param parsed_args:
        :return:
        """
        self.command = parsed_args.command
        self.wait = parsed_args.wait
        self.show_output = parsed_args.show_output
        self.pod = parsed_args.pod
        self.environment = parsed_args.environment
        self.region = parsed_args.region
        self.bucket_name = parsed_args.bucket_name
        self.deployement_key = parsed_args.deployment_key
        if self.deployement_key:
            self.targets = [
                {
                    'Key' : "tag:athenahealth:datafabric:deploymentKey",
                    'Values' : [self.deployement_key]
                }
            ]
            self.get_pod_environment_from_deployment_key()
        else:
            self.pod = parsed_args.pod
            self.environment = parsed_args.environment

        if parsed_args.instance_ids is not None:
            for instance_id in parsed_args.instance_ids:
                self.instances.append(instance_id)

        if parsed_args.tags is not None:
            for tag in parsed_args.tags:
                vals = tag.split('=')
                key = vals[0]
                value = vals[1]

                self.targets += [
                    {
                        'Key': "tag:" + key,
                        'Values': [value]
                    }
                ]

        if parsed_args.comment is not None:
            self.comment = parsed_args.comment

    def parse_parameters(self, parameters):
        self.command = parameters.get('command')
        self.wait = parameters.get('wait',True)
        self.show_output = parameters.get('show_output',True)
        self.region = parameters.get('region','us_east_1')
        if "bucket_name" in parameters:
            self.bucket_name=parameters.get('bucket_name')

        self.deployement_key = parameters.get('deployment_key')
        if self.deployement_key:
            self.get_pod_environment_from_deployment_key()
        else:
            self.pod = parameters.get('pod')
            self.environment = parameters.get('environment')

        self.instances = parameters.get('instance_ids',[])
        if self.deployement_key:
            self.targets = [
                {
                    'Key' : "tag:athenahealth:datafabric:deploymentKey",
                    'Values' : [self.deployement_key]
                }
            ]
        if parameters.get('comment'):
            self.comment = parameters.get('comment')

    def _ssm_client(self):

        if self.ssm_client is None:
            aws_connection=AWSConnectionFactory(self.environment,self.region,self.pod)
            self.ssm_client = aws_connection.get_client('ssm')

        return self.ssm_client

    def invoke(self):
        """Perform the actual SSM calls and console output.
        :return:
        """

        payload={
            "Targets" : self.targets,
            "DocumentName" : "AWS-RunShellScript",
            "Comment" : self.comment,
            "Parameters" : {"commands" : self.command},
        }
        if len(self.bucket_name)>0:
            payload['OutputS3BucketName']=self.bucket_name

        command_result = self._ssm_client().send_command(**payload)
        # command_result = self._ssm_client().send_command(Targets=self.targets,
        #                                                  InstanceIds=self.instances,
        #                                                  DocumentName='AWS-RunShellScript',
        #                                                  Comment=self.comment,
        #                                                  Parameters={"commands": [self.command]},
        # )

        command_id = command_result["Command"]["CommandId"]
        status = command_result["Command"]["Status"]

        print("Executed command '{}' - {}  ({})".format(self.command, command_id, status))

        for tag in self.targets:

            key = tag["Key"]
            value = tag["Values"]

            print("   - {} = {}".format(key, value))

        if self.wait or self.show_output:

            not_done = True
            in_error = False

            while not_done:
                results = self._ssm_client().list_commands(CommandId=command_id)

                for result in results["Commands"]:
                    status = result['Status']
                    status_details = result['StatusDetails']
                    target_count = result['TargetCount']
                    target_complete = result['CompletedCount']
                    target_error = result["ErrorCount"]

                    print(" - {} ({}) [{} total, {} complete, {} error]".format(status, status_details, target_count,
                                                                                target_complete, target_error))

                    # if status in self.SUCCESS_STATES:
                    #     not_done = False
                    #
                    #     if status_details in self.ERROR_DETAIL_STATES:
                    #         in_error = True
                    #
                    # elif status in self.ERROR_STATES:
                    #     not_done = False
                    #     in_error = True
                    if (target_count==target_complete) and status in self.STATES:
                        not_done = False

                if not_done:
                    time.sleep(5)



            invocations = self._ssm_client().list_command_invocations(CommandId=command_id)
            if self.show_output:
                print("Command output")

            responses=[]
            for invocation in invocations["CommandInvocations"]:
                instance_id = invocation['InstanceId']
                instance_name = invocation['InstanceName']
                status = invocation['Status']

                response = self._ssm_client().get_command_invocation(
                    CommandId=command_id,
                    InstanceId=instance_id
                )
                responses.append(response)
                try:
                    elapsed_time = response["ExecutionElapsedTime"]
                    response_code = response["ResponseCode"]

                    standard_output_content = response["StandardOutputContent"]
                    standard_error_content = response["StandardErrorContent"]

                    if self.show_output:
                        print(" - [{} in {}] {} ({})".format(status, elapsed_time, instance_id, instance_name))
                        if response_code == 0:
                           print(standard_output_content)
                        else:
                            print(standard_error_content)
                except Exception as error:
                    print(error)
            return responses




class AWSS3:
    def __init__(self,pod, environment, region):
        self.pod=pod
        self.environmet=environment
        self.region=region
        self.aws_connection=AWSConnectionFactory(self.environmet,self.region,self.pod)
        self.debug=False

        self.client = self.aws_connection.get_client('s3')
        self.resource = self.aws_connection.get_resource('s3')


    def empty_bucket(self, bucket_name):
        print("Empty bucket: {}".format(bucket_name))
        bucket = self.resource.Bucket(bucket_name)
        bucket.objects.all().delete()

    def delete_bucket(self, bucket_name):
        self.empty_bucket(bucket_name)
        print("Delete S3 bucket: {}".format(bucket_name))
        response = self.client.delete_bucket(
            Bucket=bucket_name
        )
        return response

    def create_bucket(self, bucket_name):
        print("Create S3 bucket: {}".format(bucket_name))
        response = self.client.create_bucket(Bucket=bucket_name)
        return response

    def assert_dir_exists(self, path):
        """
        Checks if directory tree in path exists. If not it created them.
        :param path: the path to check if it exists
        """
        try:
            os.makedirs(path)
        except OSError as e:
            pass


    def download_dir(self, url):
        """
        Downloads recursively the given S3 URL to the local directory.
        :param url: S3 URL
        """
        target=os.path.join(os.getcwd(),'output')
        url_list = url.split('/')
        bucket=url_list[3]
        print('/'.join(url_list[4:]))
        path='/'.join(url_list[4:])
        # Handle missing / at end of prefix
        if not path.endswith('/'):
            path = '/'.join(path.split('/')[:-1])+'/'



        paginator = self.client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=bucket, Prefix=path):
            # Download each file individually
            for key in result['Contents']:
                # Calculate relative path
                rel_path = key['Key'][len(path):]
                # Skip paths ending in /
                if not key['Key'].endswith('/'):
                    local_file_path = os.path.join(target, rel_path)
                    # Make sure directories exist
                    local_file_dir = os.path.dirname(local_file_path)
                    self.assert_dir_exists(local_file_dir)
                    self.client.download_file(bucket, key['Key'], local_file_path)


    def download_file(self, url, file_name):
        url_list = url.split('/')
        bucket = url_list[3]
        path = '/'.join(url_list[4:])
        self.client.download_file(bucket, path, file_name)


class ESSupport:
    def __init__(self, deployment_key):
        self.debug=False
        self.deployment_key = deployment_key
        self.invoker = SSMInvoke()

        parse_deployment_key = self.deployment_key.split('_')
        self.pod = parse_deployment_key[0]
        self.environment=parse_deployment_key[1]

        regions = ['us_east_1', 'us_west_2']
        for region in regions:
            if self.deployment_key.find(region)>-1:
                self.region=region

        self.bucket_name = self.deployment_key.replace('_','-')[:48]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        self.s3_client = AWSS3(self.pod,self.environment,self.region)


    def get_backup_bucket(self):
        payload = {
            "show_output" : True,
            "command": ["docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_snapshot/_all'"],
            "deployment_key": self.deployment_key
        }
        self.invoker.parse_parameters(payload)
        responses = self.invoker.invoke()
        for response in responses:
            result = json.loads(response.get('StandardOutputContent'))
            if result.get('error'):
                print("Error encountered")
                return None
            else:
                s3 = (result.get('s3_repository').get('settings'))
                bucket_name = s3.get('bucket')
                return bucket_name

    def get_cluster_stats(self):
        self.s3_client.create_bucket(self.bucket_name)
        try:
            payload = {
                "command": [
                    "echo 'IP: ' $(hostname -i)",
                    "echo '\n***Health***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/health?v'",
                    "echo '\n***Nodes***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/nodes?v'",
                    "echo '\n***Allocation***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/allocation?v'",
                    "echo '\n***Document Count***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/count?v'",
                    "echo '\n***Fielddata***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/fielddata?v'",
                    "echo '\n***Pending Tasks***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/pending_tasks?v'",
                    "echo '\n***Thread pool***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/thread_pool?v'",
                    "echo '\n***Plugins***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/plugins?v&s=component&h=name,component,version,description'",
                    "echo '\n***Backup Location***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_snapshot/_all'",
                    "echo '\n***Snapshots***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/_snapshot/s3_repository?v'",
                    "echo '\n***Indices***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/indices?v'",
                    "echo '\n***Indices***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/shards?v'",
                    "echo '\n***Segments***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/segments?v'",
                    "echo '\n***Templates***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/templates?v'",
                    "echo '\n***Stats***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_nodes/stats?pretty'",
                    "echo '\n***Recovery***'",
                    "docker exec $(docker ps -qf 'name=elastic') bash -c 'curl -s -u $DB_ADMIN:$DB_ADMIN_PASSWORD $(hostname -i):9200/_cat/recovery?v'",
                    "echo '\n***Logs***'",
                    "docker logs $(docker ps -qf 'name=elastic')"
                    ],
                "deployment_key": self.deployment_key,
                "bucket_name" : self.bucket_name,
                "show_output" : False
            }
            self.invoker.parse_parameters(payload)
            responses = self.invoker.invoke()
            for response in responses:
                URL = response.get('StandardOutputUrl')
                instance_id = response.get('InstanceId')
                output_dir = os.path.join(os.getcwd(),self.bucket_name)
                self.s3_client.assert_dir_exists(output_dir)
                output_file = os.path.join(output_dir,instance_id)
                self.s3_client.download_file(URL,output_file)
                print("Saving output to {}".format(output_file))
        except Exception as error:
            print(error)
        finally:
            self.s3_client.delete_bucket(self.bucket_name)


def main():
    parser = argparse.ArgumentParser(description = 'Gather Elasticsearch cluster information')
    parser.add_argument('--deployment_key', action='store', help="Deployment Key", required=True)


    results = parser.parse_args()

    if results.deployment_key:
        es = ESSupport(results.deployment_key)
        es.get_cluster_stats()



if __name__ == '__main__':
    main()




