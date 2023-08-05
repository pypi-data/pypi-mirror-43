# -*- coding: utf-8 -*-

import json

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# CloudFormationRegionConfig
########################################

class CloudFormationRegionConfig(RegionConfig):
    """
    CloudFormation configuration for a single AWS region
    """
    stacks = {}

    def parse_stack(self, global_params, region, stack):
        """
        Parse a single stack and fetch additional attributes

        :param stack:
        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        """
        stack['id'] = stack.pop('StackId')
        stack['name'] = stack.pop('StackName')

        stack_description = api_clients[region].describe_stacks(StackName=stack['name'])
        stack['termination_protection'] = stack_description['Stacks'][0]['EnableTerminationProtection']
        stack['drifted'] = stack.pop('DriftInformation')['StackDriftStatus'] == 'DRIFTED'

        template = api_clients[region].get_template(StackName=stack['name'])['TemplateBody']['Resources']
        stack['deletion_policy'] = 'Delete'
        for group in template.keys():
            if 'DeletionPolicy' in template[group]:
                stack['deletion_policy'] = template[group]['DeletionPolicy']
                break

        stack_policy = api_clients[region].get_stack_policy(StackName=stack['name'])
        if 'StackPolicyBody' in stack_policy:
            stack['policy'] = json.loads(stack_policy['StackPolicyBody'])
        self.stacks[stack['name']] = stack


########################################
# CloudFormationConfig
########################################

class CloudFormationConfig(RegionalServiceConfig):
    """
    CloudFormation configuration for all AWS regions
    """

    region_config_class = CloudFormationRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(CloudFormationConfig, self).__init__(service_metadata, thread_config)
