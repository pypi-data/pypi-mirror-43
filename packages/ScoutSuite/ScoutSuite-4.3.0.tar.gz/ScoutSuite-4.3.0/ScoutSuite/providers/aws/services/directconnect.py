# -*- coding: utf-8 -*-

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig


########################################
# DirectConnectRegionConfig
########################################

class DirectConnectRegionConfig(RegionConfig):
    """
    DirectConnect configuration for a single AWS region
    """
    connections = {}

    def parse_connection(self, global_params, region, connection):
        """
        Parse a single connection and fetch additional attributes

        :param connection:
        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        """
        connection['id'] = connection.pop('connectionId')
        connection['name'] = connection.pop('connectionName')
        self.connections[connection['id']] = connection


########################################
# DirectConnectConfig
########################################

class DirectConnectConfig(RegionalServiceConfig):
    """
    DirectConnect configuration for all AWS regions
    """

    region_config_class = DirectConnectRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(DirectConnectConfig, self).__init__(service_metadata, thread_config)
