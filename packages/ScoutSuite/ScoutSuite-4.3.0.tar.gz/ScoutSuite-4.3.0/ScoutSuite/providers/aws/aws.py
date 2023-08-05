# -*- coding: utf-8 -*-

import time
from collections import Counter

import boto3
from botocore.session import Session

from ScoutSuite.core.console import print_info, print_exception


def build_region_list(service, chosen_regions=None, partition_name='aws'):
    """
    Build the list of target region names

    :param service:
    :param chosen_regions:
    :param partition_name:

    :return:
    """
    if chosen_regions is None:
        chosen_regions = []
    service = 'ec2containerservice' if service == 'ecs' else service
    # Get list of regions from botocore
    regions = Session().get_available_regions(service, partition_name=partition_name)
    if len(chosen_regions):
        return list((Counter(regions) & Counter(chosen_regions)).elements())
    else:
        return regions


def connect_service(service, credentials, region_name=None, config=None, silent=False):
    """
    Instantiates an AWS API client

    :param service:                         Service targeted, e.g. ec2
    :param credentials:                     Id, secret, token
    :param region_name:                     Region desired, e.g. us-east-2
    :param config:                          Configuration (optional)
    :param silent:                          Whether or not to print messages

    :return:
    """
    api_client = None
    try:
        client_params = {'service_name': service.lower()}
        session_params = {'aws_access_key_id': credentials.get('access_key'),
                          'aws_secret_access_key': credentials.get('secret_key'),
                          'aws_session_token': credentials.get('token')}
        if region_name:
            client_params['region_name'] = region_name
            session_params['region_name'] = region_name
        if config:
            client_params['config'] = config
        aws_session = boto3.session.Session(**session_params)
        if not silent:
            info_message = 'Connecting to AWS %s' % service
            if region_name:
                info_message = info_message + ' in %s' % region_name
            print_info('%s...' % info_message)
        api_client = aws_session.client(**client_params)
    except Exception as e:
        print_exception(e)
    return api_client


def get_name(src, dst, default_attribute):
    """

    :param src:
    :param dst:
    :param default_attribute:

    :return:
    """
    name_found = False
    if 'Tags' in src:
        for tag in src['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] != '':
                dst['name'] = tag['Value']
                name_found = True
    if not name_found:
        dst['name'] = src[default_attribute]
    return dst['name']


def get_caller_identity(credentials):
    api_client = connect_service('sts', credentials, silent=True)
    return api_client.get_caller_identity()


def get_aws_account_id(credentials):
    caller_identity = get_caller_identity(credentials)
    return caller_identity['Arn'].split(':')[4]


def get_partition_name(credentials):
    caller_identity = get_caller_identity(credentials)
    return caller_identity['Arn'].split(':')[1]


def handle_truncated_response(callback, params, entities):
    """
    Handle truncated responses

    :param callback:
    :param params:
    :param entities:

    :return:
    """
    results = {}
    for entity in entities:
        results[entity] = []
    while True:
        try:
            marker_found = False
            response = callback(**params)
            for entity in entities:
                if entity in response:
                    results[entity] = results[entity] + response[entity]
            for marker_name in ['NextToken', 'Marker', 'PaginationToken']:
                if marker_name in response and response[marker_name]:
                    params[marker_name] = response[marker_name]
                    marker_found = True
            if not marker_found:
                break
        except Exception as e:
            if is_throttled(e):
                time.sleep(1)
            else:
                raise e
    return results


def is_throttled(e):
    """
    Determines whether the exception is due to API throttling.

    :param e:                           Exception raised
    :return:                            True if it's a throttling exception else False
    """
    return (hasattr(e, 'response') and 'Error' in e.response and e.response['Error']['Code'] in
            ['Throttling', 'RequestLimitExceeded', 'ThrottlingException', 'TooManyRequestsException'])
