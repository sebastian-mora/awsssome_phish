import json

import boto3
import os
import time

from decimal import Decimal

def create_oidc_application(sso_oidc_client):
    print("Creating temporary AWS SSO OIDC application")
    client = sso_oidc_client.register_client(
        clientName='aws-org-mapper',
        clientType='public'
    )
    client_id = client.get('clientId')
    client_secret = client.get('clientSecret')
    return client_id, client_secret


def initiate_device_code_flow(sso_oidc_client,oidc_application, start_url):
    print("Initiating device code flow")
    authz = sso_oidc_client.start_device_authorization(
        clientId=oidc_application[0],
        clientSecret=oidc_application[1],
        startUrl=start_url
    )

    url = authz.get('verificationUriComplete')
    deviceCode = authz.get('deviceCode')
    return url, deviceCode


def create_device_code_url(sso_oidc_client, start_url):
    oidc_application = create_oidc_application(sso_oidc_client)
    url, device_code = initiate_device_code_flow(
        sso_oidc_client, oidc_application, start_url)
    return url, device_code, oidc_application

def save_to_db(url, deviceCode, oidc_application):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sessionTable')

    data={
        'deviceCode': deviceCode,
        'url': url,
        'urlClicked': Decimal(time.time()),
        'sessionCaptured': False,
        'oidc_app': oidc_application,
        'token': '',
        'urlExpires': Decimal(time.time() + 600)
    }

    table.put_item(
    Item=data
    )

    return data

def main(event, context):

    START_URL = os.environ['START_URL']
    REGION = os.environ['REGION']
    sso_oidc_client = boto3.client('sso-oidc', region_name=REGION)

    url, device_code, oidc_application = create_device_code_url(sso_oidc_client, START_URL)

    save_to_db(url, device_code, oidc_application)

    response = {
        "statusCode": 301,
        "headers":{
            "Location": url
        }
    }

    return response
