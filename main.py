#!/usr/bin/env python3
import boto3
import botocore.credentials
from botocore.awsrequest import AWSRequest
from botocore.httpsession import URLLib3Session
from botocore.auth import SigV4Auth
import datetime
import json
import xmltodict
import argparse


def main():
    site = get_site()
    request = AWSRequest(method='GET', url=get_api_url(),
                         params=get_params(site), headers=get_headers())

    SigV4Auth(get_credentials(), 'awis', 'us-west-1').add_auth(request)
    res = URLLib3Session().send(request.prepare())
    json = parse_respose(res.content)
    print(json)


def get_site():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', type=str, required=True,
                        help='Site name to link in')

    args = parser.parse_args()
    return args.site


def get_api_url(): return 'https://awis.amazonaws.com/api'


def get_headers(): return {
    'Host': 'awis.us-west-1.amazonaws.com',
    'x-amz-date': datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
}


def get_params(site): return {
    'Action': 'SitesLinkingIn',
    'ResponseGroup': 'SitesLinkingIn',
    'Url': site
}


def get_credentials():
    session = boto3.Session()
    credentials = session.get_credentials().get_frozen_credentials()
    return credentials


def parse_respose(xml):
    result = xmltodict.parse(xml)
    data = json.dumps(result).replace('@', '')
    return json.loads(data)


if __name__ == '__main__':
    main()
